<?xml version="1.0" encoding="UTF-8"?>
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
      <Paragraph Style="Bold">
       <Elements>
        <Text>
         <Content>УСФР в Красногвардейском районе Белгородской области</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="NormalSmall">
       <Elements>
        <Text>
         <Content>(наименование территориального органа Фонда пенсионного и социального страхования Российской Федерации)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Bold">
       <Elements>
        <Text>
         <Content>Заявление</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Bold">
       <Elements>
        <Text>
         <Content>об аннулировании ранее поданного заявления</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Bold">
       <Elements>
        <Text>
         <Content>Иванова Елена Васильевна</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="NormalSmall">
       <Elements>
        <Text>
         <Content>(фамилия, имя, отчество (при наличии))</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Bold">
       <Elements>
        <Text>
         <Content>1. Статус МАТЬ</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>(мать, мужчина – единственный усыновитель, мужчина, воспитывающий детей1 , отец2 , ребенок3 – указать</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="NormalSmall">
       <Elements>
        <Text>
         <Content>нужное)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Bold">
       <Elements>
        <Text>
         <Content>2. Дата рождения лица, получившего сертификат 25.01.1987</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Bold">
       <Elements>
        <Text>
         <Content><xsl:value-of select="/document/InfoPanel/snils"/><xsl:text>&#32;</xsl:text></Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>000-000-000 01</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Bold">
       <Elements>
        <Text>
         <Content>4. Серия и номер сертификата МК-8 0000003</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Bold">
       <Elements>
        <Text>
         <Content>5. Сертификат выдан УСФР в Красногвардейском районе Белгородской области, 10.08.2016</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>(кем и когда выдан)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Bold">
       <Elements>
        <Text>
         <Content>6. Документ, удостоверяющий личность Паспорт гражданина РФ, 0405 №666289</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>(наименование, серия (при наличии) и номер документа)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>УВД г.Бирюч 10.09.2005</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>(кем и когда выдан)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Bold">
       <Elements>
        <Text>
         <Content>7. Адрес места жительства 666131, г. Бирюч, пер.. Луговой, д. 92, кв. 115</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>(почтовый индекс, наименование региона, района, города, иного населенного пункта, улицы, номера дома, корпуса, квартиры, на</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>основании записи в паспорте или документе, подтверждающем регистрацию по месту жительства, места пребывания (если</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>предъявляется не паспорт, а иной документ, удостоверяющий личность), фактического проживания)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Bold">
       <Elements>
        <Text>
         <Content>8. Адрес электронной почты, контактный телефон 8 (905) 976-17-34</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Bold">
       <Elements>
        <Text>
         <Content>9. Дата рождения (усыновления) ребенка, в связи с рождением (усыновлением) которого возникло право на</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Normal">
       <Elements>
        <Text>
         <Content>дополнительные меры государственной поддержки</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>10.06.2016</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="NormalSmall">
       <Elements>
        <Text>
         <Content>(число, месяц, год)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Bold">
       <Elements>
        <Text>
         <Content>10. Сведения о представителе</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>(фамилия, имя, отчество (при наличии), дата рождения)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>(почтовый адрес места жительства (пребывания), фактического проживания)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Bold">
       <Elements>
        <Text>
         <Content>11. Тип представителя</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>(указать нужное - законный представитель/доверенное лицо)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Bold">
       <Elements>
        <Text>
         <Content>12. Адрес электронной почты, контактный телефон представителя</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Bold">
       <Elements>
        <Text>
         <Content>13. Документ, удостоверяющий личность представителя</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>(наименование, серия (при наличии) и номер документа, кем и когда выдан)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Bold">
       <Elements>
        <Text>
         <Content>14. Документ, подтверждающий полномочия представителя</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>(наименование, серия (при наличии) и номер документа, кем и когда выдан)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>___________________________________________</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="NormalSmall">
       <Elements>
        <Text>
         <Content>1 указывается при возникновении права при смерти матери, не имеющей гражданства Российской Федерации</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="NormalSmall">
       <Elements>
        <Text>
         <Content>2 указывается при возникновении права в случае прекращения права у матери</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="NormalSmall">
       <Elements>
        <Text>
         <Content>3 указывается при возникновении права в случае прекращения права у матери или отца</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Normal">
       <Elements>
        <Text>
         <Content>Страница 1 из 2</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Normal">
       <Elements>
        <Text>
         <Content>Прошу аннулировать ранее поданное заявление</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>от 13.12.2016 № 141466</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Normal">
       <Elements>
        <Text>
         <Content>20.01.2017 Иванова Елена Васильевна</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>(дата) (подпись заявителя)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Normal">
       <Elements>
        <Text>
         <Content>Сидорова Ольга Валерьевна</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="NormalSmall">
       <Elements>
        <Text>
         <Content>(подпись специалиста)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="NormalSmall">
       <Elements>
        <Text>
         <Content>Заявление гражданки (гражданина)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Normal">
       <Elements>
        <Text>
         <Content>зарегистрировано 16</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>(регистрационный номер заявления)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Normal">
       <Elements>
        <Text>
         <Content>Принял</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Normal">
       <Elements>
        <Text>
         <Content>20.01.2017 Сидорова Ольга Валерьевна</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>(дата приема заявления) (подпись специалиста) (ФИО специалиста)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="NormalSmall">
       <Elements>
        <Text>
         <Content>(линия отреза)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="NormalSmall">
       <Elements>
        <Text>
         <Content>Расписка-уведомление (извещение)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="NormalSmall">
       <Elements>
        <Text>
         <Content>Заявление об аннулировании ранее поданного заявления о распоряжении средствами материнского (семейного)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="NormalSmall">
       <Elements>
        <Text>
         <Content>капитала гражданки (гражданина)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Normal">
       <Elements>
        <Text>
         <Content>зарегистрировано 16</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>(регистрационный номер заявления)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Normal">
       <Elements>
        <Text>
         <Content>Принял</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Normal">
       <Elements>
        <Text>
         <Content>20.01.2017 Сидорова Ольга Валерьевна</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Underline">
       <Elements>
        <Text>
         <Content>(дата приема заявления) (подпись специалиста) (ФИО специалиста)</Content>
        </Text>
       </Elements>
      </Paragraph>
      <Paragraph Style="Normal">
       <Elements>
        <Text>
         <Content>Страница 2 из 2</Content>
        </Text>
       </Elements>
      </Paragraph>

     </Elements>
    </Section>
   </Sections>
  </Document>
 </xsl:template>
</xsl:stylesheet>
