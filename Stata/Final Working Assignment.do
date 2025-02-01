// The assignment

cd D:\Lab\Stata

// br respondent_age age_1 age_2 age_3 age_4 age_5 random_mem_id agegroup



use "SCS_data.dta" , clear

// 1. Create age group for respondents (agegroup): //////////////////////////////////////////////////////////////////////////////
generate respondent_age = . 


forvalues i = 1/17 {
    replace respondent_age = age_`i' if random_mem_id == "`i'"
}


gen agegroup = .

replace agegroup = 1 if respondent_age < 5
replace agegroup = 2 if inrange(respondent_age, 6, 12)
replace agegroup = 3 if inrange(respondent_age, 13, 18)
replace agegroup = 4 if inrange(respondent_age, 19, 30)
replace agegroup = 5 if inrange(respondent_age, 31, 45)
replace agegroup = 6 if inrange(respondent_age, 46, 60)
replace agegroup = 7 if respondent_age > 60


// 2. Create total contact variable (allnoncontact) //////////////////////////////////////////////////////////////////////////////


//br meet_people_1 meet_people_2 meet_people_3 meet_people_4 place_house_1 place_house_2 place_house_3 place_house_4
// br meet_people_1 meet_people_2 meet_people_3
// br enumid meet_people_1 meet_people_2 meet_people_3 allnoncontact
// br allnoncontact

// drop allnoncontact

egen allnoncontact = rowtotal(meet_people_*) 


//foreach var of varlist meet_people_* {
//    replace allnoncontact = allnoncontact + `var'
//}

// to check if you are correct 
//list meet_people_* allnoncontact if allnoncontact > 0


// 3. Create a variable identifying the day of the survey date (day) //////////////////////////////////////////////////////////////////////////////


//drop prev_day
//drop day_of_week

generate prev_day = startdate - 1
generate day_of_week = dow(prev_day) //dow returens the day of the week like 0 Sunday , 1 Monday

generate day = ""
replace day = "Friday" if day_of_week == 5
replace day = "Saturday" if day_of_week == 6
replace day = "Weekday" if day_of_week >= 0 & day_of_week <= 4


// 4. Create sex variable (sex) //////////////////////////////////////////////////////////////////////////////

//substr(string, start, length)

//br enumid village_strata

generate strata_code = real(substr(village_strata, strpos(village_strata, "-") + 1, .))

generate sex = ""
replace sex = "Female" if inlist(strata_code, 1, 3, 5)
replace sex = "Male" if inlist(strata_code, 2, 4, 6)

//br enumid  village_strata  sex

//5.  //////////////////////////////////////////////////////////////////////////////


* Create a new variable for each age group
drop allnoncontact_male
drop allnoncontact_female
gen allnoncontact_male = allnoncontact if sex == "Male"
gen allnoncontact_female = allnoncontact if sex == "Female"




summarize allnoncontact if agegroup == 1, detail
local group_median = r(p50)

display `group_median'

summarize allnoncontact, detail
local overall_median = r(p50)

	  
	  
//5 Final try 

* First, calculate the frequencies for each age group
bysort agegroup: gen group_count = _N if !missing(agegroup)

* Replace the agegroup variable with descriptive labels
gen agegroup_label = ""
replace agegroup_label = "<5 years (N=" + string(group_count) + ")" if agegroup == 1
replace agegroup_label = "6-12 years (N=" + string(group_count) + ")" if agegroup == 2
replace agegroup_label = "13-18 years (N=" + string(group_count) + ")" if agegroup == 3
replace agegroup_label = "19-30 years (N=" + string(group_count) + ")" if agegroup == 4
replace agegroup_label = "31-45 years (N=" + string(group_count) + ")" if agegroup == 5
replace agegroup_label = "46-60 years (N=" + string(group_count) + ")" if agegroup == 6
replace agegroup_label = ">60 years (N=" + string(group_count) + ")" if agegroup == 7

encode agegroup_label,  gen(agegroup_label_num)



twoway (histogram allnoncontact if sex_num == 2 , color(blue%50) percent width(5) by(agegroup_label_num)) ///
	   (histogram allnoncontact if sex_num ==  1 , color(red%50) percent width(5) by(agegroup_label_num)) 


	   
// levelsof agegroup_label_num, local(agegroups)
// foreach age in `agegroups' {
//     twoway (histogram allnoncontact if sex_num == 2 & agegroup_label_num == `age', color(blue%50) percent width(5) ///
//             xline(`group_median', lpattern(dash) lcolor(black))) ///
//            (histogram allnoncontact if sex_num == 1 & agegroup_label_num == `age', color(red%50) percent width(5) ///
//             xline(`overall_median', lpattern(dash) lcolor(red)))
// }
//	   
// 




// 6 
/// table sex day, statistic(mean allnoncontact) gender is strinig need to convert it to number 

encode sex, gen(sex_num)
encode day, gen(day_num)


table sex_num day_num, statistic(mean allnoncontact)
collect export "nonhousehold_contacts_by_sex_day.xlsx", replace










save "SCS_data.dta" , replace 













