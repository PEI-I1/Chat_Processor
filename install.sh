python_cmd="python3"

$python_cmd -m venv env
source ./env/bin/activate
pip install -r requirements.txt
$python_cmd -m deeppavlov install ner_ontonotes_bert_mult
