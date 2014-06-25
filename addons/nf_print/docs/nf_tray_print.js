function NFPrint(theDoc)
{

	var special_tag = "nfprinternamespecialtag";
        try  {
		var currentPrinter="";
		for (var i=0; i<theDoc.numPages; i++){
                	var str = "";
			var n = this.getPageNumWords(i);
			for(var j=0;j<n;j++) {
				var wd = this.getPageNthWord(i, j, true);
	//			app.alert(wd);
				if (wd.indexOf(special_tag)!=-1){
					currentPrinter = wd.substring(special_tag.length,wd.length);
	//				app.alert("Tag Found ;-)"+currentPrinter);
					break;
				}
			}
			var pp = theDoc.getPrintParams();
			pp.firstPage = i;
			pp.lastPage = i;
			pp.pageHandling = pp.constants.handling.none;
			pp.interactive = pp.constants.interactionLevel.silent;
			var fv = pp.constants.flagValues;
			//pp.flags |= fv.setPageSize;
			if (currentPrinter!="")
				pp.printerName = currentPrinter;
			//pp.printerName="Brother-HL-5270DN"
	//		app.alert("printing on : |"+pp.printerName+"|");
			theDoc.print(pp);
        		//theDoc.print({bUI: false, bSilent: true, bShrinkToFit: false});
		}


        } catch (e)  {
                app.alert("Exception: "+e)
        };





}

// Add a menu item
app.addMenuItem( { cName: "NF_INFO:OpenERPTrayPrint", cUser: "NF Tray Print", cParent: "File", 
    cbPrepend: false,
    nPos: "Print",
    cEnable: "event.rc = (event.target != null);",
    cExec: "NFPrint(event.target)" });
// you can execute this menu item from other programs such as IAC VB / VC code.


