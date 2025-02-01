// Graph Tutorial

cd "D:\Lab\Stata"

sysuse auto, clear


graph bar price


graph bar price, over(foreign)

graph bar price, over(foreign) stack

graph bar price, over(foreign) asyvars


graph bar (percent) price, over(foreign)


//graph (percent) bar price mpg, over(foreign)
graph  bar price mpg, over(foreign)


graph bar price, over(foreign) title("Car Prices") subtitle("By Type") note("Source: Auto Dataset")



graph bar price, over(foreign) ytitle("Price in USD") ylabel(0(5000)20000)

graph bar price, over(foreign) bar(1, color(red))

drop avg_price
egen avg_price = mean(price), by(foreign)
graph bar (mean) price, over(foreign) ytitle("Average Price")


// Histo 

histogram mpg

histogram mpg, percent

histogram mpg, normal

histogram mpg, bin(10) title("Distribution of MPG") xlabel(0(5)50) ylabel(, angle(0))

histogram mpg, by(foreign)


gen is_foreign = foreign == 1
label define foreign_label 0 "Domestic" 1 "Foreign"
label values is_foreign foreign_label

twoway (histogram mpg if is_foreign==0, width(2) fcolor(blue%50)) ///
       (histogram mpg if is_foreign==1, width(2) fcolor(red%50)), ///
       legend(order(1 "Domestic" 2 "Foreign")) ///
       title("Overlay of MPG by Car Type")

	   
histogram mpg, percent by(foreign, total) title("MPG Distribution by Car Type")

/// stuff i need


histogram mpg, percent

histogram mpg, by(foreign, total)

generate is_foreign = foreign == 1
label define foreign_label 0 "Domestic" 1 "Foreign"
label values is_foreign foreign_label


twoway (histogram mpg if is_foreign==0, width(2) fcolor(blue%50)) ///
       (histogram mpg if is_foreign==1, width(2) fcolor(red%50)), ///
       legend(order(1 "Domestic Cars" 2 "Foreign Cars") ///
              position(6) title("Car Type") size(medium) nobox col(1)) ///
       title("Overlay of MPG by Car Type")

histogram mpg, by(foreign , total) percent
