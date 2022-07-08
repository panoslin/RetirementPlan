# Family Financial Application

Calculate future cashflow via `time value of money`

- Build Excel table (pandas DataFrame) 
base on expense and income 
- Run optimization on the 
rate of return from investment porofolio 
and the raising rate of salary 
- Estimate and set the Family Financial Goal 
in a Financial Statements(.xlsx)

## Algorithm

1. Inflation and Investment

    All of our money will deflate, 
    meaning that 100 unit of currency 
    will worth less in the future. 
    
    To prevent the deflation of our money. 
    we need to invest our money into different baskets 
    to gain excess yield, 
    such as bond, stock, bank deposit, insurance and etc. 
    And we call those baskets to be your investment portfolio.
        
        Here we discount all the future cashflow to now 
        with inflation rate of 5% 
    
1. Expense
    
    Calculate the future expenses with escalation rate
        
        Besides necessary living expenses (food, housing), 
        we also introduce unavoidable expenses like:
        recreation, wedding, car, house and etc.  
        
        But the living expense is not fixed, 
        we always want a more quality life, 
        hence we also set a annual escalation rate of 5% 
        to represent the "upgrading" of our life.
    
2. Income

    Fix income coming from work  
    
    There will always be a ceil for fix income coming from work,  
    so we set a ceiling income.
    
    The remainging question is, when will we meet the ceiling?  
    
        We Calculate the raising rate of salary 
        using COBYLA optimazation algorithm 
        (same for rate of return from investment portfolio)
    
  