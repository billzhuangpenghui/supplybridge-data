import requests
import pymysql


if __name__ == '__main__':
    # api_key
    api_key = 'bc5c62e6-00aa-426e-adca-7f70abe513eb'
    # company_api
    company_api_url = 'https://piloterr.com/api/v2/linkedin/company/info'

    integrate_url = 'https://docs.piloterr.com/api/request'

    company_id = '1675'
    # 定义API请求参数和Header
    data = {'method': 'GET', 'url': company_api_url, 'params': {'query': company_id}, 'headers': {'x-api-key': api_key}}
    headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
    cookies = {'session_id': 'xxxxxxxx'}

    # mysql 数据库配置
    mysql_host = '120.25.207.139'
    mysql_port = 3306
    mysql_user = 'root'
    mysql_password = 'root_password'
    mysql_database = 'dbcec_stock_center0'

    response = requests.post(integrate_url, json=data, headers=headers, cookies=cookies)
    print('invoke api result : ', response)

    result = response.json()
    print('invoke api json result : ', result)

    result_data = result['response']

    if not result_data:
        print('there is nothing is result')

    insert_sql = """INSERT INTO `dbcec_stock_center0`.`dbcec_company_info` (`company_id`, `company_url`, `company_name`, `logo_url`, `website`, `specialities`, `industry`, `tagline`, `description`, `founded`, `staff_range`, `staff_count`, `follower_count`, `headquarter`, `associated_hashtags`, `showcase_companies`, `similar_companies`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    db = pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, password=mysql_password,
                         database=mysql_database)

    cursor = db.cursor()

    insert_param = (result_data['company_id'], result_data['company_url'], result_data['company_name'], result_data['logo_url'], result_data['website'], ",".join(result_data['specialities']), result_data['industry'], result_data['tagline'],result_data['description'],result_data['founded'], result_data['staff_range'], result_data['staff_count'],result_data['follower_count'],str(result_data['headquarter']), str(result_data['associated_hashtags']), str(result_data['showcase_companies']), str(result_data['similar_companies']))

    res_num = cursor.execute(insert_sql, insert_param)

    cursor.close()

    db.commit()

    db.close()