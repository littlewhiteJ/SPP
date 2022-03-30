from utils import *
# local import
import baostock as bs

# download strategy: we will donwload data in the whole year even though we just need data in one day
class DownloadData():
    def __init__(self, config):
        self.config = config
        # get stock list
        with open(self.config.stock_list_file, 'r') as f:
            self.stock_list = json.load(f)
        
    def download_baostock(self, stock_list, year_list):
        # logging in
        baostock_lg = bs.login()
        logging.debug(baostock_lg.error_code)
        logging.debug(baostock_lg.error_msg)

        logging.info('start to download baostock')
        # generate rs according to stock_list and date_list
        for stock_code in stock_list:
            for year in year_list:
                # adjustflag={1:forward adjustment,2:backward adjustment,3:no adjustment}
                # we use backward adjustment here
                # generate start_date, end_date
                start_date = '-'.join([year, '01', '01'])
                end_date = '-'.join([year, '12', '31'])
                
                rs = bs.query_history_k_data(stock_code,
                                            "date,open,high,low,close,preclose,volume,amount\
                                            ,turn,tradestatus,pctChg,peTTM,psTTM,pcfNcfTTM,pbMRQ,isST",
                                            start_date=start_date, end_date=end_date,
                                            frequency="d", adjustflag="2") 
                logging.debug(rs.error_code)
                logging.debug(rs.error_msg)
                
                result_list = []
                while (rs.error_code == '0') & rs.next():
                    result_list.append(rs.get_row_data())
                result = pd.DataFrame(result_list, columns=rs.fields)
                # generate this_filename
                this_filename = '_'.join([stock_code, year]) + '.csv'
                result.to_csv(os.path.join(self.config.rawdata_home, this_filename), encoding="gbk", index=False)

        bs.logout()
        logging.info('end.')
    
    def get_year_list(self):
        whole_year_list = set()
        
        periods = self.config.train_period + self.config.test_period
        for p in periods:
            year_list = [str(year) for year in range(int(p[:4]), 1 + int(p[9:13]))]
            whole_year_list |= set(year_list)
        return list(whole_year_list)
        
    def run(self):
        # get year list from train period and test period
        year_list = self.get_year_list()
        
        logging.info('start all download')
        
        # check use_factor
        for u_factor in self.config.use_factor:
            if u_factor == 'baostock':
                self.download_baostock(self.stock_list, year_list)
            else:
                # other data source
                pass
    
        logging.info('finish all download')
        
if __name__ == '__main__':
    config = Config('/home/mokou/SPP/config/base_config.json')
    config.run()
    
    download_data = DownloadData(config)
    download_data.run()
    

