from pathlib import Path
import json,subprocess,sys,unittest

ROOT=Path(__file__).resolve().parents[1]/'skills/deepseen-xixing'
class LanguageTests(unittest.TestCase):
    def test_english_fixture_runs_in_isolation(self):
        r=subprocess.run([sys.executable,'-I','-S','-X','utf8',str(ROOT/'scripts/check_distillation.py'),'--catalog',str(ROOT/'assets/demo/catalog.en.json'),'--lang','en'],capture_output=True,encoding='utf-8')
        self.assertEqual(r.returncode,0,r.stderr)
        data=json.loads(r.stdout);self.assertEqual(data['units'],4)
        self.assertIn('limitsEn',data);self.assertNotIn('limitsZh',data)
    def test_chinese_remains_default(self):
        r=subprocess.run([sys.executable,'-X','utf8',str(ROOT/'scripts/check_distillation.py'),'--catalog',str(ROOT/'assets/demo/catalog.json')],capture_output=True,encoding='utf-8')
        self.assertEqual(r.returncode,0,r.stderr);self.assertIn('limitsZh',json.loads(r.stdout))
if __name__=='__main__':unittest.main()
