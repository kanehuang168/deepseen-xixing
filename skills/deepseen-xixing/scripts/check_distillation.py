"""Read-only structural checks; this does not judge source meaning or method quality."""
import argparse
import hashlib
import json
from pathlib import Path


def relative_file(root, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('来源与交付位置必须是非空相对路径')
    path = Path(value.split('#', 1)[0])
    resolved = (root / path).resolve()
    if path.is_absolute() or not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
        raise ValueError('来源或交付文件缺失，或路径超出本次记录目录')
    return resolved


def check_catalog(catalog, root):
    if not isinstance(catalog, dict):
        raise ValueError('候选记录必须是对象')
    source = catalog.get('source', {})
    if not isinstance(source, dict):
        raise ValueError('来源记录必须是对象')
    source_path = relative_file(root, source.get('file'))
    if source.get('sha256') != hashlib.sha256(source_path.read_bytes()).hexdigest():
        raise ValueError('来源指纹已改变，旧候选关联需要复核')
    source_text = source_path.read_text(encoding='utf-8')
    tasks = catalog.get('sourceTasks')
    units = catalog.get('units')
    if not isinstance(tasks, list) or not tasks or not isinstance(units, list) or not units:
        raise ValueError('需要明确的来源任务和候选/参考去向记录')
    if not all(isinstance(t, dict) and isinstance(t.get('id'), str) and t['id'].strip() for t in tasks):
        raise ValueError('来源任务必须有稳定编号')
    task_ids = [t['id'] for t in tasks]
    if len(set(task_ids)) != len(task_ids):
        raise ValueError('来源任务编号重复')
    seen, covered, counts = set(), set(), {}
    for unit in units:
        if not isinstance(unit, dict):
            raise ValueError('候选条目必须是对象')
        uid = unit.get('id')
        if not isinstance(uid, str) or not uid.strip() or uid in seen:
            raise ValueError('方法编号缺失或重复')
        seen.add(uid)
        references = unit.get('sourceTasks')
        if not isinstance(references, list) or not references or not all(isinstance(x,str) and x in task_ids for x in references):
            raise ValueError('候选必须关联已声明的来源任务')
        covered.update(references)
        locator = unit.get('evidenceLocator')
        if not isinstance(locator,str) or not locator.strip() or locator not in source_text:
            raise ValueError('出处定位缺失或未在所给文本中找到')
        disposition = unit.get('disposition')
        if disposition not in ('CANDIDATE', 'REFERENCE', 'NEEDS_EVIDENCE', 'REJECTED'):
            raise ValueError('必须区分候选、参考、待补证与不采用')
        counts[disposition] = counts.get(disposition,0) + 1
        if disposition in ('CANDIDATE','REFERENCE'):
            relative_file(root, unit.get('destination'))
        elif not isinstance(unit.get('reason'),str) or not unit['reason'].strip():
            raise ValueError('待补证或不采用项需要明确理由')
    missing = sorted(set(task_ids) - covered)
    if missing:
        raise ValueError('声明的重要来源任务缺少去向：' + '、'.join(missing))
    return {'status':'STRUCTURE_CHECK_PASSED','sourceSha256':source['sha256'],'sourceTasks':len(task_ids),'units':len(units),'dispositions':counts,'limitsZh':'仅检查所声明记录的结构、指纹、文件去向与覆盖；不证明来源语义、许可、方法效果、完整来源覆盖或发布资格。'}


def main():
    parser=argparse.ArgumentParser(description='只读检查本地方法蒸馏记录，不联网、不执行来源脚本')
    parser.add_argument('--catalog',type=Path,required=True)
    args=parser.parse_args()
    try:
        catalog=json.loads(args.catalog.read_text(encoding='utf-8'))
        print(json.dumps(check_catalog(catalog,args.catalog.parent),ensure_ascii=False,indent=2))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print('结构检查未完成：'+str(error))
        return 2
    return 0


if __name__=='__main__':
    raise SystemExit(main())
