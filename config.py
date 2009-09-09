import ConfigParser

def config_default(conffile):
    config = ConfigParser.RawConfigParser()
    config.add_section('settings')
    config.set('settings', 'InputDataFile', 'in_data.skv')
    config.set('settings', 'OutputDataFile', 'out_data.skv')
    
    config.add_section('authentication')
    config.set('authentication', 'CustomerNumber', '')
    config.set('authentication', 'Username', '')
    config.set('authentication', 'Password', '')

    config.write(open(conffile, 'wb'))
    
if __name__ == '__main__':
    config_default('ljorderse.conf')