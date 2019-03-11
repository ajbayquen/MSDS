library(ggplot2)
library(dplyr)
library(plotly)
library(shiny)

df <- read.csv('https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv')


ui <- fluidPage(
  headerPanel('Mortality Rate Over Time Per State vs. National Average'),
  sidebarPanel(
    selectInput('ICD', 'ICD.Chapter', unique(df$ICD.Chapter), selected='Certain infectious and parasitic diseases'),
    selectInput('ST', 'State', unique(df$State), selected='AL')
  ),
  mainPanel(
    plotOutput('plot1')
  )
)



server <- function(input, output) {

  output$plot1 <- renderPlot({
    
  
    dfslice <- df %>% 
      filter(State==input$ST, ICD.Chapter==input$ICD)
    usavg <- df %>% 
      filter(ICD.Chapter==input$ICD) %>% 
      group_by(Year) %>% 
      summarise(rateyr=(sum(as.numeric(Deaths))/sum(as.numeric(Population))*100000))
    
    ggplot(dfslice, aes(x=Year, y=Crude.Rate, color='blue')) + 
      geom_line(size=3) + 
      geom_line(aes(x=usavg$Year, y=usavg$rateyr, color='red'),size=2) + 
      scale_color_manual(
        name='Legend', 
        values=c('blue'='blue', 'red'='red'), 
        labels=c('State','U.S. Average' ))

    
  })
  
}

shinyApp(ui = ui, server = server)


