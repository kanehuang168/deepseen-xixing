import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/deepseen-xixing'
spec=importlib.util.spec_from_file_location('check_distillation',SKILL/'scripts/check_distillation.py')
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)


class DistillationRecordTests(unittest.TestCase):
    def setUp(self):
        self.root=SKILL/'assets/demo'
        self.catalog=json.loads((self.root/'catalog.json').read_text(encoding='utf-8'))

    def test_complete_sample_accounts_for_candidate_reference_and_rejection(self):
        result=checker.check_catalog(self.catalog,self.root)
        self.assertEqual(result['dispositions'],{'CANDIDATE':2,'REFERENCE':1,'REJECTED':1})

    def test_unexplained_source_task_cannot_disappear(self):
        self.catalog['sourceTasks'].append({'id':'new-task'})
        with self.assertRaises(ValueError):checker.check_catalog(self.catalog,self.root)

    def test_duplicate_method_identity_is_rejected(self):
        self.catalog['units'].append(copy.deepcopy(self.catalog['units'][0]))
        with self.assertRaises(ValueError):checker.check_catalog(self.catalog,self.root)

    def test_changed_source_invalidates_old_link(self):
        self.catalog['source']['sha256']='0'*64
        with self.assertRaises(ValueError):checker.check_catalog(self.catalog,self.root)

    def test_missing_destination_is_rejected(self):
        self.catalog['units'][0]['destination']='does-not-exist.md'
        with self.assertRaises(ValueError):checker.check_catalog(self.catalog,self.root)

    def test_destination_must_stay_inside_current_record_directory(self):
        with self.assertRaises(ValueError):checker.relative_file(self.root,'../../SKILL.md')


if __name__=='__main__':unittest.main()
