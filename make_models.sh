python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_md
python intent/make_model.py
python intent/__init__.py
python -m spacy train ner/model.cfg --training.max_epochs 15 --nlp.batch_size 64 --training.optimizer.@optimizers RAdam.v1 --output ner/out
rm -rf ner_model
mv ner/out/model-best ner_model
deactivate