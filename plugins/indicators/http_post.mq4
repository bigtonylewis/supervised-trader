//+------------------------------------------------------------------+
//|                                                    http_post.mq4 |
//|                       Copyright ?2006, MetaQuotes Software Corp. |
//|                                        http://www.metaquotes.net |
//+------------------------------------------------------------------+
#property copyright "Copyright ?2012, Jianing YANG."
#property link      "http://blog.jianingy.com"

#property indicator_chart_window
//--- input parameters
extern string    api = "http://guru.corp.linuxnote.net:9999/forex/tick";
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
#include <ghttp.mqh>

int last_update = 0;

int init()
  {
//---- indicators
//----
   return(0);
  }
//+------------------------------------------------------------------+
//| Custom indicator deinitialization function                       |
//+------------------------------------------------------------------+
int deinit()
  {
//----
   
//----
   return(0);
  }
//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
//+------------------------------------------------------------------+
int start()
  {
   string http_url;
   string query;
   string response;
   int    pos = 1;
   int    counted_bars = IndicatorCounted();
//----
   // if (counted_bars < 0) return(-1);
   if (Time[pos] == last_update) return (0);
   
   query = StringConcatenate("Time=", Time[pos],
                             "&Period=", Period(),
                             "&Symbol=", Symbol(),
                             "&Open=", Open[pos],
                             "&Close=", Close[pos],
                             "&High=", High[pos],
                             "&Low=", Low[pos]);
   
   http_url = StringConcatenate(api, "?", query);
   Print(http_url);
   HttpGET(http_url, response);
   last_update = Time[pos];
//----
   return(0);
  }
//+------------------------------------------------------------------+
