library(ggplot2)
library(dplyr)
library(plotly)
library(shiny)

df <- read.csv('https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv')


ui <- fluidPage(
  headerPanel('Mortality Rate per ICD Chapter for all U.S. States (in Desceding Mortality Rate Order)'),
  sidebarPanel(
    selectInput('ICD', 'ICD.Chapter', unique(df$ICD.Chapter), selected='Certain infectious and parasitic diseases'),
    selectInput('Year', 'Year', unique(df$Year), selected=2010)
  ),
  mainPanel(
    plotlyOutput('plot1')
    )
)

server <- function(input, output, session) {
  
  selectedData <- reactive({
    dfSlice <- df %>%
      filter(ICD.Chapter == input$ICD, Year == input$Year)  
  
 
    
  })
  
  output$plot1 <- renderPlotly({
    
    dfSlice <- df %>%
      filter(ICD.Chapter == input$ICD, Year == input$Year)  
    
    dfSlice$State <- factor(dfSlice$State, levels = unique(dfSlice$State)[order(dfSlice$Crude.Rate, decreasing = TRUE)])
    
    plot_ly(dfSlice, y = ~Crude.Rate, x = ~State,  type='bar')
            
  })
  
 
  
}

shinyApp(ui = ui, server = server)


