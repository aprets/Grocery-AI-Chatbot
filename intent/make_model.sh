rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_md
python make_model.py
python test_import.py
deactivate