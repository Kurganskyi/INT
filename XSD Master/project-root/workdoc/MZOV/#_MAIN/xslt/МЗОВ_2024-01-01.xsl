<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="1.0">
    <xsl:output method="html" indent="yes" encoding="utf-8"/>
    <xsl:include href="МЗОВ_2024-01-01.inc.xsl"/>
    <xsl:template match="/">
        <xsl:text disable-output-escaping='yes'>&lt;!DOCTYPE html></xsl:text>
        <html lang="ru">
            <head>
                <link rel="stylesheet" type="text/css" href="AFStyles/CommonAFStyle.css"/>
                <link rel="stylesheet" type="text/css" href="AFStyles/A4Portrait.css"/>
                <meta charset="utf-8"/>
                <meta name="application name" content="Альбом форматов СФР"/>
                <title>Заявление об отказе от получения ежемесячной выплаты в связи с рождением (усыновлением) ребенка до достижения им возраста трех лет из средств материнского (семейного) капитала</title>
            </head>
            <body>
                <xsl:call-template name="inc"/>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>