//+------------------------------------------------------------------+
//|                                                    http_post.mq4 |
//|                       Copyright ?2006, MetaQuotes Software Corp. |
//|                                        http://www.metaquotes.net |
//+------------------------------------------------------------------+
#property copyright "Copyright ?2012, Jianing YANG."
#property link      "http://blog.jianingy.com"

#property indicator_chart_window
//--- input parameters
extern string    api = "http://192.168.155.1:8080/";
extern string broker_timezone = "+2";

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
   IndicatorDigits(Digits);
   
   // convert broker timestamp to GMT timestamp
   int gmt_time = Time[pos] - 3600 * StrToInteger(broker_timezone);
   query = StringConcatenate("time=", gmt_time,
                             "&period=", Period(),
                             "&symbol=", Symbol(),
                             "&open=", DoubleToStr(Open[pos], Digits),
                             "&close=", DoubleToStr(Close[pos], Digits),
                             "&high=", DoubleToStr(High[pos], Digits),
                             "&low=", DoubleToStr(Low[pos], Digits),
                             "&volume=", Volume[pos]);
   
   http_url = StringConcatenate(api, "?", query);
   Print(http_url);
   HttpGET(http_url, response);
   last_update = Time[pos];
   Print(response);
//----
   return(0);
  }
//+------------------------------------------------------------------+