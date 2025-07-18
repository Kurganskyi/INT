<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs УТ7 ПР8 sig ns1" version="1.0" xmlns:УТ7="http://пф.рф/УТ/2023-04-03" xmlns:ПР8="http://пф.рф/Представитель/2024-01-01" xmlns:sig="http://iis.ecp.ru/SignInfo/2023-01-10" xmlns:ns1="http://пф.рф/ВВ/МСК/МЗОВ/2024-01-01">
	<xsl:output method="html" indent="yes" encoding="utf-8"/>
	<xsl:include href="../../Общие/УнифТипы_2023-04-03.xsl"/>
	<xsl:include href="../../Общие/Базовые.xsl"/>
	<xsl:template match="/" name="inc">
		<xsl:variable name="vForm" select="/ns1:ЭДСФР/ns1:МЗОВ"/>
		<div class="afWrap pfrAfMZOV">
			<h1 class="afHeader">Заявление<br/>об отказе от получения ежемесячной выплаты в связи<br/>с рождением (усыновлением) ребенка до достижения им возраста<br/> трех лет из средств материнского (семейного) капитала</h1>
			<p class="afInterval"/>
			<p class="afInterval"/>
			<p class="afInterval"/>
			<p class="afInterval"/>
			<p class="afParagraph">Прошу прекратить выплату ежемесячной выплаты в связи с рождением (усыновлением) ребенка до достижения им возраста трех лет из средств материнского (семейного) капитала (далее – ежемесячная выплата).</p>
			<p class="afInterval"/>
			<div class="afRow afCenterBlock">1. Сведения о заявителе</div>
			<p class="afInterval"/>
			<div class="afRow">
				<div class="afCol-1-3 afC">Фамилия </div>
				<div class="afCol-2-3 afValue afUnderlinedBlock">
					<xsl:value-of select="$vForm/ns1:Заявитель/УТ7:ФИО/УТ7:Фамилия"/>
				</div>
			</div>
			<div class="afRow">
				<div class="afCol-1-3 afC">Имя </div>
				<div class="afCol-2-3 afValue afUnderlinedBlock">
					<xsl:value-of select="$vForm/ns1:Заявитель/УТ7:ФИО/УТ7:Имя"/>
				</div>
			</div>
			<div class="afRow">
				<div class="afCol-1-3 afC">Отчество (при наличии) </div>
				<div class="afCol-2-3 afValue afUnderlinedBlock">
					<xsl:value-of select="$vForm/ns1:Заявитель/УТ7:ФИО/УТ7:Отчество"/>
				</div>
			</div>
			<div class="afRow">
				<div class="afCol-1-3 afC">СНИЛС </div>
				<div class="afCol-2-3 afValue afUnderlinedBlock">
					<xsl:value-of select="$vForm/ns1:Заявитель/УТ7:СНИЛС"/>
				</div>
			</div>
			<div class="afRow">
				<div class="afCol-1-3 afC">Дата рождения (дд.мм.гггг) </div>
				<div class="afCol-2-3 afValue afUnderlinedBlock">
					<xsl:choose>
						<xsl:when test="$vForm/ns1:Заявитель/УТ7:ДатаРождения">
							<xsl:call-template name="Date2GOST">
								<xsl:with-param name="pDate" select="$vForm/ns1:Заявитель/УТ7:ДатаРождения"/>
							</xsl:call-template>
						</xsl:when>
						<xsl:when test="$vForm/ns1:Заявитель/УТ7:ДатаРожденияОсобая">
							<xsl:call-template name="УТ7:DateSpecialStr">
								<xsl:with-param name="pDate" select="$vForm/ns1:Заявитель/УТ7:ДатаРожденияОсобая"/>
							</xsl:call-template>
						</xsl:when>
						<xsl:otherwise>&#160;</xsl:otherwise>
					</xsl:choose>
				</div>
			</div>
			<div class="afRow">
				<div class="afCol-1-3 afC">Сведения о документе, удостоверяющем личность <br/>(наименование, дата выдачи, реквизиты)</div>
				<div class="afCol-2-3 afValue afUnderlinedBlock">
					<br/><br/>
					<xsl:if test="$vForm/ns1:Заявитель/УТ7:УдостоверяющийДокумент">
						<xsl:call-template name="CodDULStr">
							<xsl:with-param name="pCodDocument" select="$vForm/ns1:Заявитель/УТ7:УдостоверяющийДокумент/УТ7:Код"/>
						</xsl:call-template>,&#160;
						 <xsl:call-template name="Date2GOST">
							<xsl:with-param name="pDate" select="$vForm/ns1:Заявитель/УТ7:УдостоверяющийДокумент/УТ7:ДатаВыдачи"/>
						</xsl:call-template>,&#160;
						<xsl:if test="$vForm/ns1:Заявитель/УТ7:УдостоверяющийДокумент/УТ7:Серия">
							<xsl:value-of select="$vForm/ns1:Заявитель/УТ7:УдостоверяющийДокумент/УТ7:Серия"/>&#160; 
						</xsl:if>
						№<xsl:value-of select="$vForm/ns1:Заявитель/УТ7:УдостоверяющийДокумент/УТ7:Номер"/>,&#160;
                        <xsl:value-of select="$vForm/ns1:Заявитель/УТ7:УдостоверяющийДокумент/УТ7:КемВыдан"/>
					</xsl:if>
				</div>
			</div>
			<div class="afRow">
				<div class="afCol-1-3 afC">Адрес электронной почты,<br/> контактный телефон </div>
				<div class="afCol-2-3 afValue afUnderlinedBlock">
					<br/>
					<xsl:if test="$vForm/ns1:Заявитель/УТ7:АдресЭлПочты">
						<xsl:value-of select="$vForm/ns1:Заявитель/УТ7:АдресЭлПочты"/>&#160;
					</xsl:if>
					<xsl:value-of select="$vForm/ns1:Заявитель/УТ7:Телефон"/>
				</div>
			</div>
			<p class="afInterval"/>
			<p class="afInterval"/>
			<p class="afInterval"/>
			<div class="afRow afCenterBlock">2. Сведения о ребенке, на которого осуществлялась ежемесячная выплата<br/>
												в связи с рождением (усыновлением) ребенка до достижения им возраста<br/>
													трех лет из средств материнского (семейного) капитала
			</div>
			<p class="afInterval"/>
			<div class="afRow">
				<div class="afCol-1-3 afC">Фамилия </div>
				<div class="afCol-2-3 afValue afUnderlinedBlock">
					<xsl:value-of select="$vForm/ns1:СертифицируемыйРебенок/УТ7:ФИО/УТ7:Фамилия"/>
				</div>
			</div>
			<div class="afRow">
				<div class="afCol-1-3 afC">Имя </div>
				<div class="afCol-2-3 afValue afUnderlinedBlock">
					<xsl:value-of select="$vForm/ns1:СертифицируемыйРебенок/УТ7:ФИО/УТ7:Имя"/>
				</div>
			</div>
			<div class="afRow">
				<div class="afCol-1-3 afC">Отчество (при наличии) </div>
				<div class="afCol-2-3 afValue afUnderlinedBlock">
					<xsl:value-of select="$vForm/ns1:СертифицируемыйРебенок/УТ7:ФИО/УТ7:Отчество"/>
				</div>
			</div>
			<div class="afRow">
				<div class="afCol-1-3 afC">СНИЛС </div>
				<div class="afCol-2-3 afValue afUnderlinedBlock">
					<xsl:value-of select="$vForm/ns1:СертифицируемыйРебенок/УТ7:СНИЛС"/>
				</div>
			</div>
			<div class="afRow">
				<div class="afCol-1-3 afC">Дата рождения (дд.мм.гггг) </div>
				<div class="afCol-2-3 afValue afUnderlinedBlock">
					<xsl:choose>
						<xsl:when test="$vForm/ns1:СертифицируемыйРебенок/УТ7:ДатаРождения">
							<xsl:call-template name="Date2GOST">
								<xsl:with-param name="pDate" select="$vForm/ns1:СертифицируемыйРебенок/УТ7:ДатаРождения"/>
							</xsl:call-template>
						</xsl:when>
						<xsl:when test="$vForm/ns1:СертифицируемыйРебенок/УТ7:ДатаРожденияОсобая">
							<xsl:call-template name="УТ7:DateSpecialStr">
								<xsl:with-param name="pDate" select="$vForm/ns1:СертифицируемыйРебенок/УТ7:ДатаРожденияОсобая"/>
							</xsl:call-template>
						</xsl:when>
						<xsl:otherwise>&#160;</xsl:otherwise>
					</xsl:choose>
				</div>
			</div>
			<xsl:choose>
				<xsl:when test="ns1:ЭДСФР/ns1:МЗОВ/ns1:Представитель">
					<div class="afNoBreakInside">
						<p class="afInterval"/>
						<div class="afRow afCenterBlock">3. Сведения о представителе заявителя<sup class="afFootnote">*</sup>
						</div>
						<p class="afInterval"/>
						<div class="afRow">
							<div class="afCol-1-3 afC">Фамилия</div>
							<div class="afCol-2-3 afValue afUnderlinedBlock">
								<xsl:value-of select="$vForm/ns1:Представитель/ПР8:АнкетныеДанные/УТ7:ФИО/УТ7:Фамилия"/>
							</div>
						</div>
						<div class="afRow">
							<div class="afCol-1-3 afC">Имя</div>
							<div class="afCol-2-3 afValue afUnderlinedBlock">
								<xsl:value-of select="$vForm/ns1:Представитель/ПР8:АнкетныеДанные/УТ7:ФИО/УТ7:Имя"/>
							</div>
						</div>
						<div class="afRow">
							<div class="afCol-1-3 afC">Отчество (при наличии)</div>
							<div class="afCol-2-3 afValue afUnderlinedBlock">
								<xsl:value-of select="$vForm/ns1:Представитель/ПР8:АнкетныеДанные/УТ7:ФИО/УТ7:Отчество"/>
							</div>
						</div>
						<div class="afRow">
							<div class="afCol-1-3 afC">Тип представителя (указать нужное - законный представитель/доверенное лицо)</div>
							<div class="afCol-2-3 afValue afUnderlinedBlock">
								<br/>
								<xsl:choose>
									<xsl:when test="$vForm/ns1:Представитель/ПР8:Тип/ПР8:ЗаконныйПР">законный представитель</xsl:when>
									<xsl:when test="$vForm/ns1:Представитель/ПР8:Тип/ПР8:ДоверенноеЛицо">доверенное лицо</xsl:when>
									<xsl:otherwise>&#160;</xsl:otherwise>
								</xsl:choose>
							</div>
						</div>
						<div class="afRow">
							<div class="afCol-1-3 afC">СНИЛС</div>
							<div class="afCol-2-3 afValue afUnderlinedBlock">
								<xsl:value-of select="$vForm/ns1:Представитель/ПР8:АнкетныеДанные/УТ7:СНИЛС"/>
							</div>
						</div>
						<div class="afRow">
							<div class="afCol-1-3 afC">Дата рождения (дд.мм.гггг) </div>
							<div class="afCol-2-3 afValue afUnderlinedBlock">
								<xsl:choose>
									<xsl:when test="$vForm/ns1:Представитель/ПР8:АнкетныеДанные/УТ7:ДатаРождения">
										<xsl:call-template name="Date2GOST">
											<xsl:with-param name="pDate" select="$vForm/ns1:Представитель/ПР8:АнкетныеДанные/УТ7:ДатаРождения"/>
										</xsl:call-template>
									</xsl:when>
									<xsl:when test="$vForm/ns1:Представитель/ПР8:АнкетныеДанные/УТ7:ДатаРожденияОсобая">
										<xsl:call-template name="УТ7:DateSpecialStr">
											<xsl:with-param name="pDate" select="$vForm/ns1:Представитель/ПР8:АнкетныеДанные/УТ7:ДатаРожденияОсобая"/>
										</xsl:call-template>
									</xsl:when>
									<xsl:otherwise>&#160;</xsl:otherwise>
								</xsl:choose>
							</div>
						</div>
						<div class="afRow">
							<div class="afCol-1-3">Сведения о документе, удостоверяющем личность <br/>(наименование, дата выдачи, реквизиты)</div>
							<div class="afCol-2-3 afValue afUnderlinedBlock">
								<br/><br/>
								<xsl:if test="$vForm/ns1:Представитель/ПР8:АнкетныеДанные/УТ7:УдостоверяющийДокумент">
									<xsl:call-template name="УТ7:CodDocumentStr">
										<xsl:with-param name="pCodDocument" select="$vForm/ns1:Представитель/ПР8:АнкетныеДанные/УТ7:УдостоверяющийДокумент"/>
									</xsl:call-template>,&#160;
								<xsl:call-template name="Date2GOST">
									<xsl:with-param name="pDate" select="$vForm/ns1:Представитель/ПР8:АнкетныеДанные/УТ7:УдостоверяющийДокумент/УТ7:ДатаВыдачи"/>
								</xsl:call-template>,&#160;
                                <xsl:if test="$vForm/ns1:Представитель/ПР8:АнкетныеДанные/УТ7:УдостоверяющийДокумент/УТ7:Серия">
										<xsl:value-of select="$vForm/ns1:Представитель/ПР8:АнкетныеДанные/УТ7:УдостоверяющийДокумент/УТ7:Серия"/>&#160; 
                                </xsl:if>
									№<xsl:value-of select="$vForm/ns1:Представитель/ПР8:АнкетныеДанные/УТ7:УдостоверяющийДокумент/УТ7:Номер"/>,&#160; 
                                <xsl:value-of select="$vForm/ns1:Представитель/ПР8:АнкетныеДанные/УТ7:УдостоверяющийДокумент/УТ7:КемВыдан"/>
								</xsl:if>
							</div>
						</div>
						<div class="afRow">
							<div class="afCol-1-3">Сведения о документе,<br/>подтверждающем полномочия<br/>представителя заявителя<br/>(наименование, дата выдачи, реквизиты) </div>
							<div class="afCol-2-3 afValue afUnderlinedBlock">
								<br/><br/><br/><br/>
								<xsl:if test="$vForm/ns1:Представитель/УТ7:ДокументПодтверждающийПолномочия">
									<xsl:call-template name="УТ7:CodDUP">
										<xsl:with-param name="pCod" select="$vForm/ns1:Представитель/УТ7:ДокументПодтверждающийПолномочия/УТ7:Код"/>
									</xsl:call-template>,&#160;
									<xsl:call-template name="Date2GOST">
										<xsl:with-param name="pDate" select="$vForm/ns1:Представитель/УТ7:ДокументПодтверждающийПолномочия/УТ7:ДатаВыдачи"/>
									</xsl:call-template>,&#160;
									<xsl:if test="$vForm/ns1:Представитель/УТ7:ДокументПодтверждающийПолномочия/УТ7:Серия">
										<xsl:value-of select="$vForm/ns1:Представитель/УТ7:ДокументПодтверждающийПолномочия/УТ7:Серия"/>&#160; 
									</xsl:if>
									№<xsl:value-of select="$vForm/ns1:Представитель/УТ7:ДокументПодтверждающийПолномочия/УТ7:Номер"/>,&#160; 
									<xsl:value-of select="$vForm/ns1:Представитель/УТ7:ДокументПодтверждающийПолномочия/УТ7:КемВыдан"/>
								</xsl:if>
							</div>
							<p class="afInterval"/>
						</div>
						<div class="afRow">
							<div class="afCol-1-3 afC">Адрес электронной почты,<br/>контактный телефон представителя</div>
							<div class="afCol-2-3 afValue afUnderlinedBlock">
								<br/>
								<xsl:if test="$vForm/ns1:Представитель/ПР8:АнкетныеДанные/УТ7:АдресЭлПочты">
									<xsl:value-of select="$vForm/ns1:Представитель/ПР8:АнкетныеДанные/УТ7:АдресЭлПочты"/>,&#160;
								</xsl:if>
								<xsl:value-of select="$vForm/ns1:Представитель/ПР8:АнкетныеДанные/УТ7:Телефон"/>
							</div>
						</div>
						<p class="afInterval"/>
						<p class="afInterval"/>
						<p class="afInterval"/>
						<p class="afInterval"/>
						<p class="afInterval"/>
						<div class="afRow">
							<div class="afCol-4-10">
								<div class="afC">Дата </div>
								<div class="afMarginLeft50 afValue">
									<xsl:call-template name="Date2Text">
										<xsl:with-param name="pDate" select="$vForm/ns1:ДатаЗаполнения"/>
									</xsl:call-template> г.
								</div>
							</div>
							<div class="afCol-6-10">
								<div class="afCol-1-4">&#160;</div>
								<div class="afCol-6-10">
									<div class="afUnderlinedBlock">&#160;</div>
									
								</div>
								<p class="afSubscript afCenter afMarginLeft40">(подпись заявителя (представителя заявителя)</p>
							</div>
						</div>
					</div>
					<p class="afInterval"/>
					<p class="afInterval"/>
					<p>___________________________________________</p>
					<p class="afP afFootnote">
						<span class="afSup">*</span>Заполняется в случае, если заявление подается уполномоченным представителем заявителя.</p>
				</xsl:when>
				<xsl:otherwise>
					<p class="afInterval"/>
					<p class="afInterval"/>
					<p class="afInterval"/>
					<p class="afInterval"/>
					<div class="afRow">
						<div class="afCol-4-10">
							<div class="afC">Дата </div>
							<div class="afMarginLeft50 afValue">
								<xsl:call-template name="Date2Text">
									<xsl:with-param name="pDate" select="$vForm/ns1:ДатаЗаполнения"/>
								</xsl:call-template> г.
							</div>
						</div>
						<div class="afCol-6-10">
							<div class="afCol-1-4">	&#160;</div>
							<div class="afCol-6-10">
								<div class="afUnderlinedBlock">&#160;</div>
								
							</div>
							<p class="afSubscript afCenter afMarginLeft40">(подпись заявителя)</p>
						</div>
					</div>
				</xsl:otherwise>
			</xsl:choose>
		</div>
	</xsl:template>
</xsl:stylesheet>
