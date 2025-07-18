import pdfplumber
import os
import re

pdf_path = os.path.join(os.path.dirname(__file__), 'mzaz.pdf')
output_path = os.path.join(os.path.dirname(__file__), 'mzaz_from_pdf.xslt')

# Словарь: текст из PDF -> XSLT-код (Content)
replacements = {
    "Фамилия Имя Отчество": '''
        <xsl:value-of select="/document/InfoPanel/F_Applicant"/>
        <xsl:text>&#32;</xsl:text>
        <xsl:if test="/document/InfoPanel/f_pri_r !=''">
            <xsl:text>(</xsl:text>
            <xsl:value-of select="/document/InfoPanel/f_pri_r"/>
            <xsl:text>)</xsl:text>
            <xsl:text>&#32;</xsl:text>
        </xsl:if>
        <xsl:value-of select="/document/InfoPanel/I_Applicant"/>
        <xsl:text>&#32;</xsl:text>
        <xsl:value-of select="/document/InfoPanel/Ot_Applicant"/>
    ''',
    "1. Статус": '''<xsl:value-of select="/document/InfoPanel/stat"/>''',
    "2. Дата рождения лица, получившего сертификат": '''<xsl:value-of select="substring(/document/InfoPanel/date_birth,1,10)"/>''',
    "3. Страховой номер индивидуального лицевого счета (СНИЛС)": '''<xsl:value-of select="/document/InfoPanel/snils"/><xsl:text>&#32;</xsl:text>''',
    "4. Серия и номер сертификата": '''<xsl:value-of select="/document/certificate_info/seria"/><xsl:text>&#32;</xsl:text><xsl:value-of select="/document/certificate_info/number"/>''',
    "5. Сертификат выдан": '''<xsl:value-of select="/document/certificate_info/issued_by"/><xsl:text>&#32;</xsl:text><xsl:text>код</xsl:text><xsl:text>&#32;</xsl:text><xsl:value-of select="/document/certificate_info/code"/><xsl:text>&#32;</xsl:text><xsl:value-of select="substring(/document/certificate_info/issued_date,0,11)"/>''',
    "6. Документ,удостоверяющий личность": '''<xsl:value-of select="/document/PasData/SelectTypeDoc"/><xsl:text>&#32;</xsl:text><xsl:if test="./document/PasData/SelectTypeDoc='Паспорт гражданина РФ'"><xsl:value-of select="/document/PasData/Seria_p"/><xsl:text>&#32;</xsl:text><xsl:value-of select="/document/PasData/Number_p"/></xsl:if><xsl:if test="./document/PasData/SelectTypeDoc!='Паспорт гражданина РФ'"><xsl:value-of select="/document/PasData/Seria"/><xsl:text>&#32;</xsl:text><xsl:value-of select="/document/PasData/Number"/></xsl:if>''',
    "7. Адрес места жительства": '''<xsl:if test="/document/InfoPanel/adr_reg_zayv!=''"><xsl:value-of select="/document/InfoPanel/adr_reg_zayv"/></xsl:if><xsl:if test="/document/InfoPanel/address_type='Адрес регистрации'"><xsl:value-of select="/document/InfoPanel/adr_reg_zayv_fias"/></xsl:if><xsl:if test="/document/InfoPanel/address_type='Адрес фактического проживания'"><xsl:value-of select="/document/InfoPanel/adr_fact_zayv_fias"/></xsl:if><xsl:if test="/document/InfoPanel/address_type='Адрес пребывания'"><xsl:value-of select="/document/InfoPanel/adr_preb_zayv_fias"/></xsl:if>''',
    "8. Дата рождения (усыновления) ребёнка, в связи с рождением (усыновлением) которого возникло право на дополнительные меры государственной поддержки": '''<xsl:choose><xsl:when test="./document/uk_n_v/reason ='1'"><xsl:value-of select="substring(./document/uk_n_v/date1,1,10)"/></xsl:when><xsl:otherwise><xsl:value-of select="substring(./document/uk_n_v/date2,1,10)"/></xsl:otherwise></xsl:choose>''',
    "9. Сведения о представителе": '''<xsl:value-of select="/document/predst/F_decl"/><xsl:text>&#32;</xsl:text><xsl:value-of select="/document/predst/I_decl"/><xsl:text>&#32;</xsl:text><xsl:value-of select="/document/predst/Ot_decl"/>''',
    "10. Документ,удостоверяющий личность законного представителя": '''<xsl:value-of select="/document/predst/PasData/select_doc"/>''',
    "11. Документ, подтверждающий полномочия законного представителя или доверенного лица": '''<xsl:value-of select="/document/predst/Sved_poln/Polnom_pr"/><xsl:text>&#32;</xsl:text>''',
    # Добавьте другие соответствия по необходимости
}

# Списки для определения стиля
bold_lines = [
    "Заявление",
    "об аннулировании ранее поданного заявления",
    "Иванова Елена Васильевна",
    "УСФР в Красногвардейском районе Белгородской области",
]

# Ключевые слова для подчеркивания (можно расширять)
underline_keywords = [
    "МАТЬ", "ОТЕЦ", "ЕДИНСТВЕННЫЙ", "РЕБЕНОК", "СНИЛС", "сертификат", "выдан", "паспорт", "УВД", "адрес", "телефон", "email", "почта", "тип представителя", "дата", "номер", "серия", "полномочия", "представитель", "10.", "11.", "12.", "13.", "14."
]

# Функция для определения стиля строки
def get_style(line):
    # Bold: заголовки, пункты (1., 2., ...), явно в списке
    if line in bold_lines or re.match(r"^\d+\. ", line):
        return "Bold"
    # Underline: если строка содержит ключевые слова или похожа на поле для заполнения
    if (
        any(kw.lower() in line.lower() for kw in underline_keywords)
        or re.match(r"^\d{2}\.\d{2}\.\d{4}$", line)  # дата
        or re.match(r"^\d{3}-\d{3}-\d{3} \d{2}$", line)  # СНИЛС
        or re.match(r"^[A-ZА-Я]{2}-\d+$", line)  # серия-номер
        or re.match(r"^\d+$", line)  # просто номер
        or re.match(r"^8 \(\d{3}\) \d{3}-\d{2}-\d{2}$", line)  # телефон
        or ("________________" in line)
    ):
        return "Underline"
    # NormalSmall: пояснения в скобках или мелкий текст
    if line.startswith("(") or line.endswith(")") or "указывается" in line or "при наличии" in line or "почтовый индекс" in line:
        return "NormalSmall"
    # Остальное — Normal
    return "Normal"

text = ''
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + '\n'

lines = [line.strip() for line in text.splitlines() if line.strip()]

xslt_template = '''<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl" xmlns:ms="urn:schemas-microsoft-com:xslt" xmlns:dt="urn:schemas-microsoft-com:datatypes" xmlns:nvx="http://www.netvoxlab.ru">
 <xsl:output method="xml" indent="yes"/>
 <xsl:template match="/">
  <Document xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://www.netvoxlab.ru" DefaultTabStop="0" FootnoteLocation="BottomOfPage" FootnoteNumberingRule="RestartPage" FootnoteNumberStyle="Arabic" FootnoteStartingNumber="0" UseCmykColor="false">
   <Styles>
    <Style Name="Normal">
     <ParagraphFormat SpaceAfter="0.1cm" SpaceBefore="0.1cm" Alignment="Justify"/>
     <Font Name="Arial" Size="10"/>
    </Style>
    <Style Name="NormalSmall" BaseStyle="Normal">
     <Font Size="8"/>
    </Style>
    <Style Name="Bold" BaseStyle="Normal">
     <Font Size="10" Bold="true"/>
    </Style>
    <Style Name="Italic" BaseStyle="Normal">
     <Font Size="12" Italic="true" Bold="true"/>
    </Style>
    <Style Name="ItalicSmall" BaseStyle="Normal">
     <Font Size="8" Italic="true"/>
    </Style>
    <Style Name="BoldUnderline" BaseStyle="Normal">
     <Font Size="10" Bold="true" Underline="Single"/>
    </Style>
    <Style Name="Underline" BaseStyle="Normal">
     <Font Size="10" Underline="Single"/>
    </Style>
   </Styles>
   <Sections>
    <Section>
     <Elements>
{paragraphs}
     </Elements>
    </Section>
   </Sections>
  </Document>
 </xsl:template>
</xsl:stylesheet>
'''

paragraphs = ''
for line in lines:
    content = replacements.get(line, line)
    style = get_style(line)
    paragraphs += f'      <Paragraph Style="{style}">\n       <Elements>\n        <Text>\n         <Content>{content}</Content>\n        </Text>\n       </Elements>\n      </Paragraph>\n'

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(xslt_template.replace('{paragraphs}', paragraphs))

print(f'XSLT с текстом из PDF, переменными и стилями сохранён в {output_path}') 