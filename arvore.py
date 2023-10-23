import Draft, FreeCAD, math, random, Part,Arch, FreeCADGui


interacao = 2				#Número de vezes que o algoritimo irá rodar (aumenta o numero de galhos)

diametro_tronco = 400		#Diâmetro inicial do tronco da vegetação
taxa_reducao_tronco = 0.850 #taxa na qual os galhos reduzem seu diametro

tamanho_tronco = 5000		#Altura do tronco inicial (influencia na altura e numero de galhos)
tam_max_ramos = 100			#Tamanho minimo dos galhos (influencia na quantidade de galhos)(controle sensível)

taxa_maxima_ramos = 70		#Taxa máxima de redução do tamanho dos galhos (influencia na quantidade de galhos e folhas)(controle sensível)
taxa_minima_ramos = 30		#Taxa minima de redução do tamanho dos galhos (influencia na quantidade de galhos e folhas)(controle sensível)

angulo_minimo = 40			#Ângulo minimo entre os galhos (infliencia na forma da copa)
angulo_maximo = 60			#Ângulo máximo entre os galhos (infliencia na forma da copa)

angulo_torcao = 80			#Angulo de torção dos galhos (infliencia na forma da copa)

tam_min_folhas = 600		#Tamanho minimo das folhas
tam_max_folhas = 1500		#Tamanho máximo das folhas

inclinação_max_tronco = 500	#desvio máximo do tronco inicial em relação a vertical




def ramo(comprimento, angulo, point, diametro):

	if comprimento > tam_max_ramos :
		angulo_rad = (angulo * math.pi)/180
		p1 = FreeCAD.Vector(point)
		ang2 = (random.randint(-angulo_torcao,angulo_torcao) * math.pi)/180
		p2 = FreeCAD.Vector((comprimento*math.sin(angulo_rad)+p1.x,comprimento*math.sin(ang2)+p1.y, comprimento*math.cos(angulo_rad)+p1.z))
		linha = Draft.make_wire([p1,p2], closed=False, face=False, support=None)
		linha.Label = 'linha'
		tubo = Arch.makePipe(linha)
		tubo.Diameter = diametro * taxa_reducao_tronco
		tubo.Label = 'ramo'
		diametro = diametro * taxa_reducao_tronco
		FreeCAD.ActiveDocument.recompute()

		novo_comprimento = (comprimento * random.randint(taxa_minima_ramos,taxa_maxima_ramos))/100
		novo_angulo = angulo + random.randint(angulo_minimo,angulo_maximo)
		ramo(novo_comprimento, novo_angulo, (p2.x, p2.y, p2.z), diametro)
		
		novo_comprimento = (comprimento * random.randint(taxa_minima_ramos,taxa_maxima_ramos))/100
		novo_angulo = angulo - random.randint(angulo_minimo,angulo_maximo)
		novo_angulo = novo_angulo * math.pi/180
		ang2 = (random.randint(-angulo_torcao,angulo_torcao) * math.pi)/180
		p3 = FreeCAD.Vector((comprimento*math.sin(novo_angulo)+p1.x,comprimento*math.sin(ang2)+p1.y, comprimento*math.cos(novo_angulo)+p1.z))
		linha = Draft.make_wire([p1,p3], closed=False, face=False, support=None)
		linha.Label = 'linha'
		tubo = Arch.makePipe(linha)
		tubo.Diameter = diametro
		tubo.Label = 'ramo'
		
		

		diametro = diametro * taxa_reducao_tronco
		FreeCAD.ActiveDocument.recompute()

		novo_comprimento = (comprimento * random.randint(taxa_minima_ramos,taxa_maxima_ramos))/100
		novo_angulo = angulo - random.randint(angulo_minimo,angulo_maximo)
		novo_angulo = novo_angulo * math.pi/180
		ramo(novo_comprimento, novo_angulo, (p3.x, p3.y, p3.z), diametro)

	else:
		pass
		esfera = App.ActiveDocument.addObject("Part::Sphere","folha")
		esfera.Radius = random.randint(tam_min_folhas, tam_max_folhas)
		esfera.Placement.Base = FreeCAD.Vector(point)
		esfera.ViewObject.DisplayMode = 'Shaded'
		FreeCAD.ActiveDocument.recompute()


p1 = FreeCAD.Vector(0,0,0)
p2 = FreeCAD.Vector(random.randint(-inclinação_max_tronco,inclinação_max_tronco),random.randint(-inclinação_max_tronco,inclinação_max_tronco), tamanho_tronco)

for i in range(interacao):
	ramo(tamanho_tronco,0,p2, diametro_tronco)

linha = Draft.make_wire([p1,p2], closed=False, face=False, support=None)
linha.Label = 'linha'
tubo = Arch.makePipe(linha)
tubo.Diameter = diametro_tronco
tubo.Label = 'ramo'

#agrupa o elemento gerado
lista_objetos = FreeCAD.ActiveDocument.Objects
lista_ramos = list(filter(lambda obj: 'ramo' in obj.Label, lista_objetos))
lista_folhas = list(filter(lambda obj: 'folha' in obj.Label, lista_objetos))
lista_linhas = list(filter(lambda obj: 'linha' in obj.Label, lista_objetos))

compound_ramos = App.activeDocument().addObject("Part::Compound","compound_ramos")
compound_ramos.Links = lista_ramos

compound_folhas = App.activeDocument().addObject("Part::Compound","compound_folhas")
compound_folhas.Links = lista_folhas
FreeCAD.ActiveDocument.recompute()


#cria os elementos simples
shape = compound_ramos.Shape
galhos = App.ActiveDocument.addObject('Part::Feature','galhos')
galhos.Shape = shape


shape = compound_folhas.Shape
copa = App.ActiveDocument.addObject('Part::Feature','copa')
copa.Shape = shape

galhos.ViewObject.ShapeColor = (122,78,8,0)
copa.ViewObject.ShapeColor = (130,214,41,0)

FreeCAD.ActiveDocument.recompute()
#apaga as demais formas
FreeCAD.ActiveDocument.removeObject(compound_ramos.Name)
FreeCAD.ActiveDocument.removeObject(compound_folhas.Name)

FreeCAD.ActiveDocument.recompute()
for ramo in lista_ramos:
	App.ActiveDocument.removeObject(ramo.Name)

for folha in lista_folhas:
	App.ActiveDocument.removeObject(folha.Name)

for linha in lista_linhas:
	App.ActiveDocument.removeObject(linha.Name)

# cria o compound da arvore
FreeCAD.ActiveDocument.recompute()
compound_ramos = App.activeDocument().addObject("Part::Compound","arvore")
compound_ramos.Links = [copa, galhos]

FreeCAD.ActiveDocument.recompute()