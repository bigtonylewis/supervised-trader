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
   
   /* Adjust timestamp
    *
    * Due to 'Time' returns a timestamp of broker's timezone, we have to
    * adjust it to local timezone. Let's see an example for why,
    * Consider you have a timestamp 3600 * 8 of GMT+2, if you directly apply
    * it on a GMT+0 zone, you will get a 1970-01-01 08:00:00 GMT. However, the
    * original time was 1970-01-01 10:00:00 GMT.
    *
    * To fix it, if the timestamp is s and local and broker timezone are tz1
    * and tz2. We first calculate a GMT timestamp by s - 3600 * tz1. Then we
    * calculate our local timestamp by add 3600 * tz2 to the GMT timestamp
    * which will be
    *
    * s - 3600 * tz1 + 3600 * tz2 = s - 3600 * (tz1 - tz2)
    *
    * Since there is no interface in MQ4 for getting timezone of either broker
    * or local, we can not get tz1 or tz2 directly. However, we could use API
    * TimeCurrent and TimeLocal to find the difference between tz1 and tz2.
    *
    */
   int time = Time[pos] - 3600 * (TimeHour(TimeCurrent()) - TimeHour(TimeLocal()));
   query = StringConcatenate("time=", time,
                             "&period=", Period(),
                             "&symbol=", Symbol(),
                             "&open=", Open[pos],
                             "&close=", Close[pos],
                             "&high=", High[pos],
                             "&low=", Low[pos]);
   
   http_url = StringConcatenate(api, "?", query);
   Print(http_url);
   HttpGET(http_url, response);
   last_update = Time[pos];
   Print(response);
//----
   return(0);
  }
//+------------------------------------------------------------------+