import fitz    
import re
from pathlib import Path
import pandas as pd
import json

metadata = "metadata.json" #path to metadata
dataset = "FinArg_analyst_Train.json" #path to dataset
directory = "path to folder containing analyst_report.pdf"

def content_extractor(file):
    try:
        doc = fitz.open(file)  
        content = doc.load_page(0)
        if "_JP-Morgan_" in Path(file).stem:
            areas = content.search_for("Sources for: Style Exposure")
            if not areas:
                areas = content.search_for("Source: Company data")
            if not areas:
                areas = content.search_for("Source: Company")
            if not areas:
                areas = content.search_for("analyst certification and important disclosures")
            if not areas:
                text = content.get_text("blocks")
            else:
                r=fitz.Rect(0, 50, 612, areas[0].y0)
                text = content.get_text("blocks",clip=r)

            _text = ""
            for i in text:
                if len(i[4].split())>30:
                    _text+= i[4]+'\n'
            return _text
        elif "_Capital_" in Path(file).stem:
            r=fitz.Rect(195, 0, 595, 842)
            text = content.get_text("blocks",clip=r)

            _text = ""
            for i in text:
                _text+= i[4]+'\n'
            return _text
        elif "_SinoPac-" in Path(file).stem:
            text = content.get_text("blocks")
            _text=""
            for i in text:
                if len(i[4].split())>30:
                    _text+=i[4]+'\n'
            return _text
        else:
            return None
    except Exception as e:
        print(e)
        return None

report_mapping = dict()
with open(metadata,"r") as fp:
    report_mapping = json.load(fp)

raw_content_data = dict()
with open(dataset,"r") as fp:
    anno_data = json.load(fp)
for index,instance in enumerate(anno_data):
    try:
        start_index = instance["start_index"]
        end_index = instance["end_index"]
        paragraph_num = instance["paragraph_num"]
        report_name = report_mapping[str(instance["report_id"])]
        try:
            raw_content = raw_content_data[report_name]
        except:
            raw_content = content_extractor(f"{directory}/{report_name}.pdf")
            if raw_content == None:
                continue
            raw_content_data.update({report_name:raw_content})
            
        raw_content = raw_content.split("\n\n")
        content = list()
        for text in raw_content:
            if len(text)>0:
                content.append(" ".join(text.split()))
        if len(content)==0:
            content.append("(No content)")
        anno_data[index].update({"content":content[paragraph_num][start_index:end_index+1]})
    except Exception as e:
        print(e)

with open(str(Path(dataset).with_suffix(''))+"(with_content).json","w") as fp: 
    json.dump(anno_data,fp)