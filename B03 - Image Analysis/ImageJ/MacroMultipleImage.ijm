
Dialog.create("MeuApp");
Dialog.addString("Nome do teste:", "MultiLAyer");
Dialog.addNumber("Medida Referência (pix):", 41);
Dialog.addNumber("Medida Conhecida:", 10);
Dialog.addString("Unidade de medida:", "unit");
Dialog.show()

meuTeste        = Dialog.getString();
minhaReferencia = Dialog.getNumber();
minhaMedida     = Dialog.getNumber();
minhaUnidade    = Dialog.getString();

// Importando a Imagem
open("C:/Users/idavi/Downloads/PEnO-COV816-B03-Ex02-MacroSingleImage/stack01.tiff");

// Colocando a escala pixel - unidade real
run("Set Scale...", "distance="+minhaReferencia+" known="+minhaMedida+" unit="+minhaUnidade);

// Selecionando as medidas de interesse
run("Set Measurements...", "area centroid display invert redirect=None decimal=4");


/*
 * A seguinte sequencia de passos imita o processo
 * de segmentação realizado pelo "Color Threshold"
 * com base a um esquema de cor HSB.
 * Autor: Irving D. Hernández
 * Data:  May 4, 2023 9:05:28 PM
*/

// --INICIO----------------------------------------------------------


a = getTitle();
min=newArray(3);
max=newArray(3);
filter=newArray(3);
a=getTitle();

//:> Convertindo o esquema de cor RGB para HSB
run("HSB Stack");
run("Split Channels");

//:> Renomear cada canal para facilidade de acesso
selectWindow("C1-"+a);
rename("0");
selectWindow("C2-"+a);
rename("1");
selectWindow("C3-"+a);
rename("2");

//:> Valores do canal "Hue"
min[0]=44;
max[0]=170;
filter[0]="stop";

//:> Valores do canal "Saturation"
min[1]=10;
max[1]=255;
filter[1]="pass";

//:> Valores do canal "Brightness"
min[2]=0;
max[2]=40;
filter[2]="pass";

for (i=0;i<3;i++){
  selectWindow(""+i);
  //:> Setando os valores min, max de intensidade
  setThreshold(min[i], max[i]);
  //:> Binarizar cada canal com base aos valores min, max de intensidade
  run("Make Binary", "method=Default background=Dark black stack");
  if (filter[i]=="stop"){run("Invert","stack");}
}

//:> Combinando os canais "Hue" e "Saturation"
imageCalculator("AND create stack", "0","1");
//:> Combinando o resultado (H+S) com o canal "Brightness"
imageCalculator("AND create stack", "Result of 0","2");

//:> Fechando as janelas dos canais isolados
for (i=0;i<3;i++){
  selectWindow(""+i);
  close();
}

//:> Fechando a janela do resultado "Hue" + "Saturation"
selectWindow("Result of 0");
close();

//:> Renomea a janela do segundo resultado com o nome original do Stack
selectWindow("Result of Result of 0");
rename(a);

// --FIM-------------------------------------------------------------


for (i=1; i<=nSlices; i++) {
	setSlice(i);
	run("Options...", "iterations=1 count=1 black do=Open slice");
	setOption("BlackBackground", true);
	run("Options...", "iterations=2 count=1 black do=Dilate slice");
	makeRectangle(154, 50, 640, 222);
	run("Analyze Particles...", "size=500-Infinity pixel display slice");
}

//saveAs("Results", "C:/Users/idavi/Downloads/PEnO-COV816-B03-Ex02-MacroSingleImage/Resultados/"+meuTeste+"_Results.csv");


Table.create("R2");
Table.setColumn("Idx"   , newArray(nResults()/2));
Table.setColumn("Imagem", newArray(nResults()/2));
Table.setColumn("X1"    , newArray(nResults()/2));
Table.setColumn("X2"    , newArray(nResults()/2));
Table.setColumn("S"     , newArray(nResults()/2));

a1 = getResult('X', 0);
a2 = getResult('X', 1);

for (i = 0; i < nResults()-1; i+=2) {
	
    v1 = getResult('X', i);
    v2 = getResult('X', i+1);
    d0 = abs((v1-a1)-(v2-a2));
    lb = getResultLabel(i);
    
    Table.set("Idx"   , i/2, 1+i/2);
    Table.set("Imagem", i/2, lb);
    Table.set("X1"    , i/2, v1);
    Table.set("X2"    , i/2, v2);
    Table.set("S"     , i/2, d0);
}

Table.save("C:/Users/idavi/Downloads/PEnO-COV816-B03-Ex02-MacroSingleImage/Resultados/"+meuTeste+"_Results.csv");

updateResults();

