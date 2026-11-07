简体中文 | [English](README.en.md)

# DeepSeen 吸星大法

作者：祥子｜跨境无疆 & DeepSeen AI 创始人，开发 [DeepSeen.ai](https://deepseen.ai) 跨境电商内容创作平台。

产品品牌：DeepSeen

理解获准资料、提出小范围改动，并通过实际结果验证。

## 安装与使用

```sh
npx skills add kanehuang168/deepseen-xixing
```

只查看入口：`npx skills add kanehuang168/deepseen-xixing --list`。技能正文在[SKILL.md](skills/deepseen-xixing/SKILL.md)，[自编示例](skills/deepseen-xixing/assets/trial-example.md)可独立阅读。宿主模型与工具费用以宿主为准；本包不自动调用收费服务或发布。

## 三者如何配合

公开版提供资料理解、改动建议、有限试用与证据回归的方法，并附自编的可选记录校验工具；不包含外部Skill包。

[深知灼见](https://github.com/kanehuang168/deepseen-shenzhizhuojian)负责弄清问题与方案，[项目管理](https://github.com/kanehuang168/deepseen-project-manager)负责把工作推到交付，[吸星大法](https://github.com/kanehuang168/deepseen-xixing)负责把来源与有效经验提炼为可试用方法。各自独立，不要求小任务也串行跑三遍；没有其他技能或云端工具时，本Skill仍可交付自身范围的文稿与判断。

## 能力与许可

这是面向多种业务的公开方法版；电商系列当前主要面向TikTok跨境卖家，但本系列不限定行业。Skill不会自带云端员工、长期后台运行、账号权限或付费预算；实际执行使用宿主已具备且获准的能力。

可按需访问[DeepSeen](https://deepseen.ai/?utm_source=github&utm_medium=skill&utm_campaign=xixing)了解当前实际服务；不把下载/安装数当成业务成效，本包不收集使用数据、不上传私人材料或密钥。

[MIT许可证](LICENSE)覆盖本仓库文件，不包含DeepSeen私有内核、云端服务或其他来源内容。结构/分发检查不等于方法效果、生产运行或所有宿主兼容已经验证。

平台和工具名称仅说明适用场景、格式或实际依赖，不表示合作、授权或背书；适用许可和必要版权声明仍须遵守。

## 可选方法记录工具

Python 3.10+、仅标准库，只读检查记录结构、来源指纹和交付文件。它不证明方法效果，也不自动发布或修改业务。

```sh
python -X utf8 skills/deepseen-xixing/scripts/check_distillation.py --catalog skills/deepseen-xixing/assets/demo/catalog.json
```

需要英文输出时改用`catalog.en.json --lang en`。
