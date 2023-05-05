
Dialog.create("MeuApp");
Dialog.addString("Nome do teste:", "teste");
Dialog.addNumber("Medida Conhecida:", 10);
Dialog.addNumber("Medida Referência (pix):", 41);
Dialog.addString("Unidade de medida:", "unit");
Dialog.show()

meuTeste        = Dialog.getString();
minhaMedida     = Dialog.getNumber();
minhaReferencia = Dialog.getNumber();
minhaUnidade    = Dialog.getString();

// Importando a Imagem
open("C:/Users/idavi/Downloads/PEnO-COV816-B03-Ex02-MacroSingleImage/stack01.tiff");

// Colocando a escala pixel - unidade real
run("Set Scale...", "distance="+minhaReferencia+" known="+minhaMedida+" unit="+minhaUnidade);

// Selecionando as medidas de interesse
run("Set Measurements...", "area centroid display invert redirect=None decimal=4");

// Segmentação por cor

run("Color Threshold...");
waitForUser("Operções do Usuario", "Selecione os niveis apropriados\npara segmentação por cor\nlogo pressione OK.");


for (i=1; i<nSlices; i++) {
	setSlice(i);
	run("8-bit");
	run("Options...", "iterations=2 count=1 black do=Open slice");
	setOption("BlackBackground", true);
	run("Options...", "iterations=2 count=1 black do=Dilate slice");
	makeRectangle(154, 50, 640, 222);
	run("Analyze Particles...", "display slice");
	//saveAs("Results", "C:/Users/idavi/Downloads/res/Results00"+i+".csv");
}



/*
//run("Close");
run("8-bit");
run("Options...", "iterations=2 count=1 black do=Open");
run("Options...", "iterations=1 count=1 black do=Dilate");

// Setando noss ROI
makeRectangle(154, 50, 640, 222);


//run("Analyze Particles...", "display clear");

run("Analyze Particles...", "display");
*/
saveAs("Results", "C:/Users/idavi/Downloads/PEnO-COV816-B03-Ex02-MacroSingleImage/Resultados/"+meuTeste+"_Results.csv");

