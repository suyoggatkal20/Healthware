from fpdf import FPDF
from datetime import datetime
import json

json_info = '{"email":"suyog12@gmail.com","password":"hvhjbmnb","country_code":"+91","phone":"8767564534","patient":{"first_name":"suyog","last_name":"jhdsckj","dob":"2000-07-27","gender":"M","married":"M","occupation":"Zak Marto","blood_group":"A+","education":"7th"},"address":[{"house_no":"hgjhuabiufbuwbf","locality":"gfhjaaiuabwujh"}],"emergency_contact":[{"country_code":"+91","phone_no":"85645454545454","relation":"hghbj"}],"allergies":[{"allergies":"ffgghh","description":"rr"},{"allergies":"cffffghhh","description":"fff"},{"allergies":"ffghhh","description":"ff"}],"past_diseases":[{"past_diseases":"fgyfggt","description":"gg"},{"past_diseases":"gghujjgdff","description":"ff"},{"past_diseases":"vvhhhg","description":"eer"}],"addictions":[{"addiction":"gtgyhjjj","current":true},{"addiction":"hhgfdddd","current":true},{"addiction":"fgh","current":true}],"weight":[{"weight":"12","date":"2000-07-27"}],"height":[{"height":"11","date":"2000-07-27"},{"height":"1","date":"2000-07-27"}],"cholesterol":[{"date":"2021-06-15","HDL":"55","LDL":"55"},{"date":"2021-06-16","HDL":"56","LDL":"555"},{"date":"2021-06-09","HDL":"999","LDL":"88"}],"blood_pressure":[{"date":"2021-06-09","systolic":"58","diastolic":"08"},{"date":"2021-06-09","systolic":"96","diastolic":"55"},{"date":"2021-06-09","systolic":"55","diastolic":"55"}],"glocose":[{"date":"2021-06-16","pre_meal":"88","post_meal":"88"},{"date":"2021-06-16","pre_meal":"85","post_meal":"55"},{"date":"2021-06-16","pre_meal":"85","post_meal":"88"}]}'

info1 = json.loads(json_info)


# print(info)


class PDF(FPDF):
    def header(self):
        self.image(
            "D:\Projects\Healthware\src\media\default_profile.jpg", 20, 10, 20)
        self.set_font("helvetica", 'B', 20)
        self.set_text_color(150, 27, 187)
        self.cell(0, 10, "HealthWare", align='C', ln=True)
        self.set_font('times', '', 12)
        self.set_text_color(0, 0, 0)
        self.cell(45)
        self.cell(
            0, 10, "Contact no: 1234567890, Email: abc.gmail.com", 'C', ln=True)
        self.ln(12)

    def footer(self):
        self.set_y(-20)
        self.set_font('helvetica', 'I', 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", align="L")
        self.cell(0, 10, f"Report generated on {datetime.now()}", align='R')

    def field_info(self, field1, field2):
        w = self.w / 2
        self.set_font('times', 'B', 12)
        self.cell(w - 30, 15, field1 + ":")
        self.set_font('times', '', 12)
        self.cell(w, 15, field2)
        self.ln()


def report_gen(info, path, filename):
    pdf = PDF('P', 'mm', 'A4')
    pdf.set_margins(20, 10, 20)

    pdf.set_auto_page_break(auto=True, margin=25)
    pdf.add_page()

    pdf.set_font('times', 'B', 12)
    pdf.cell(60, 10, "It is Auto-generated report pdf",
             border=True, align='C', ln=True)

    pdf.set_font('times', 'BU', 16)
    pdf.cell(40, 30, "MEDICAL REPORT", ln=True)

    pdf.ln(5)

    # basic info
    pdf.field_info("FIRST NAME", info["patient"]["first_name"])
    pdf.field_info("LAST NAME", info["patient"]["last_name"])
    pdf.field_info("EMAIL", info["user"]["email"])
    pdf.field_info("PHONE NO", info['user']
                   ["country_code"] + info['user']["phone"])
    pdf.field_info("DOB", info["patient"]["dob"])
    pdf.field_info("GENDER", info["patient"]["gender"])
    pdf.field_info("BLOOD GROUP", info["patient"]["blood_group"])
    # pdf.field_info("HEIGHT(cm)", "170")
    # pdf.field_info("WEIGHT(kg)", "61")
    pdf.field_info("MARRIAGE STATUS", info["patient"]["married"])
    pdf.field_info("OCCUPATION", info["patient"]["occupation"])
    width = pdf.w / 2
    pdf.set_font('times', 'B', 12)
    pdf.cell(width - 30, 15, "ADDRESS:")
    pdf.set_font('times', '', 12)
    pdf.multi_cell(width, 15, info["address"][0]
                   ["house_no"] + " , " + info["address"][0]["locality"])
    pdf.ln()

    # allergies
    width = pdf.w * 0.1
    pdf.set_font('times', 'B', 12)
    pdf.cell(w=0, h=15, txt="ALLERGIES:", ln=True)
    pdf.set_font('times', '', 12)

    for i in range(len(info["allergies"])):
        pdf.cell(w=width)
        pdf.cell(w=0, h=10, txt=str(i + 1) + ". Name: " +
                 info["allergies"][i]["allergies"], ln=True)
        pdf.cell(w=width)
        abc = info["allergies"][i]["description"]
        pdf.cell(w=0, h=10, txt="    Description: " +
                 abc if abc else ' None', ln=True)

    # past diseases
    width = pdf.w * 0.1
    pdf.set_font('times', 'B', 12)
    pdf.cell(w=0, h=15, txt="PAST DISEASES:", ln=True)
    pdf.set_font('times', '', 12)

    for i in range(len(info["past_diseases"])):
        pdf.cell(w=width)
        pdf.cell(w=0, h=10, txt=str(i + 1) + ". Name: " +
                 info["past_diseases"][i]["past_diseases"], ln=True)
        pdf.cell(w=width)
        abc=info["past_diseases"][i].get("description")
        pdf.cell(w=0, h=10, txt="    Description: " +
                 abc if abc else ' None', ln=True)

    # addiction
    width = pdf.w * 0.1
    pdf.set_font('times', 'B', 12)
    pdf.cell(w=0, h=15, txt="ADDICTIONS:", ln=True)
    pdf.set_font('times', '', 12)

    for i in range(len(info["addictions"])):
        pdf.cell(w=width)
        if info["addictions"][i]["current"]:
            abc=info["addictions"][i]["addiction"]
            pdf.cell(w=0,h=10, txt=str(i + 1) + ". " +
                    abc if abc else 'None', ln=True)
    print(path+filename)
    pdf.output(path+filename)


if __name__ == '__main__':
    report_gen(info1, "report/", "report.pdf")
