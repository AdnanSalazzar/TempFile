// Imports 


	
	gl nbhd	"D:\Lab\Stata"
	display "${nbhd}"
	
	//  DTA FILE 
	use "${nbhd}\SCS_data.dta", clear
	
	//excel 
	import excel "processed_data.xlsx", sheet("Sheet1") firstrow clear
	
	// CSV
	
	import delimited "main_neighborhood_list_wave1.csv", clear
	

	
	