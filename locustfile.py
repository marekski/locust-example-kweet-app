from locust import HttpLocust, TaskSet, between, task, seq_task, TaskSequence
import psycopg2, time, re


proxies = {
  'http': 'http://127.0.0.1:8087',
  'https': 'http://127.0.0.1:8087',
}

class User01Marek(TaskSequence): 
    response_date_to_create_post = ""
    response_code_to_create_post = ""

    def on_start(self):
        response = self.client.post(url="/login", headers={"Content-Type": "application/x-www-form-urlencoded"}, 
                        data="userId=marek&password=Test123%21", proxies=proxies)

        
        response_of_the_first_request = response.history[0]
        location_from_header = response_of_the_first_request.headers.get('location')

        invalid_user = False
        if('error=Invalid+username+or+password' in location_from_header):
            invalid_user = True

        if(invalid_user):
            self.client.post(
                url="/register", 
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data="userId=marek&email=marek%40mail.pl&displayName=Marek&password=Test123%21", 
                proxies=proxies)


    @seq_task(1)
    def index(self):
        self.client.get(url="/", proxies=proxies)

    
    @seq_task(2)
    def get_marek_kweets(self):
        self.client.get(url="/user/marek", proxies=proxies)


    @seq_task(3)
    def get_post_new(self):
        request = self.client.get(url="/post-new", proxies=proxies)

        content = request.content
        self.response_date_to_create_post = re.search(r'name=\"date\" value=\"(.*?)\"', str(content)).group(1)
        self.response_code_to_create_post = re.search(r'name=\"code\" value=\"(.*?)\"', str(content)).group(1)

    
    @seq_task(4)
    def post_post_new(self):
        self.client.post(url="/post-new", headers={"Content-Type": "application/x-www-form-urlencoded"}, 
                        data="date=" + self.response_date_to_create_post + "&code=" + self.response_code_to_create_post + "&text=Lorem+ipsum+from+Marek", 
                        proxies=proxies)   


    @seq_task(5)
    def get_post_new_second_request(self):
        request = self.client.get(url="/post-new", proxies=proxies)

        content = request.content
        self.response_date_to_create_post = re.search(r'name=\"date\" value=\"(.*?)\"', str(content)).group(1)
        self.response_code_to_create_post = re.search(r'name=\"code\" value=\"(.*?)\"', str(content)).group(1)

    
    @seq_task(6)
    def post_post_new_second_request(self):
        self.client.post(url="/post-new", headers={"Content-Type": "application/x-www-form-urlencoded"}, 
                        data="date=" + self.response_date_to_create_post + "&code=" + self.response_code_to_create_post + "&text=Lorem+ipsum+from+Marek", 
                        proxies=proxies)


class User02Tadeusz(TaskSequence):
    response_date_to_create_post = ""
    response_code_to_create_post = ""

    
    def on_start(self):
        response = self.client.post(url="/login", 
                                    headers={"Content-Type": "application/x-www-form-urlencoded"}, 
                                    data="userId=tadek&password=Test123%21",
                                    proxies=proxies)
        
        response_of_the_first_request = response.history[0]
        location_from_header = response_of_the_first_request.headers.get('location')

        invalid_user = False
        if('error=Invalid+username+or+password' in location_from_header):
            invalid_user = True

        if(invalid_user):
            self.client.post(
                url="/register", 
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data="userId=tadek&email=tadeusz%40mail.pl&displayName=Tadek&password=Test123%21", 
                proxies=proxies)


    @seq_task(1)
    def index(self):
        self.client.get(url="/", proxies=proxies)

    
    @seq_task(2)
    def get_marek_kweets(self):
        self.client.get(url="/user/tadek", proxies=proxies)


    @seq_task(3)
    def get_post_new(self):
        request = self.client.get(url="/post-new", proxies=proxies)

        content = request.content
        self.response_date_to_create_post = re.search(r'name=\"date\" value=\"(.*?)\"', str(content)).group(1)
        self.response_code_to_create_post = re.search(r'name=\"code\" value=\"(.*?)\"', str(content)).group(1)

    
    @seq_task(4)
    def post_post_new(self):
        self.client.post(url="/post-new", headers={"Content-Type": "application/x-www-form-urlencoded"}, 
                        data="date=" + self.response_date_to_create_post + "&code=" + self.response_code_to_create_post + "&text=Lorem+ipsum+from+Tadek", 
                        proxies=proxies)

        
class User03UniqueAleksandra(TaskSequence):
    login_id = ""
    response_date_to_create_post = ""
    response_code_to_create_post = ""

    @seq_task(1)
    def register(self):
        timestamp = time.time()
        timestamp_str = str(timestamp).replace('.', '')

        self.login_id = "ola" + timestamp_str
        email = "aleksandra" + timestamp_str + "%40mail.pl"
        display_name = "Ola"
        password = "Test123%21"

        self.client.post(
            url="/register", 
            headers={"Content-Type": "application/x-www-form-urlencoded", "Cookie": ""},
            data="userId=" + self.login_id + "&email=" + email + "&displayName=" + display_name + "&password=" + password, 
            proxies=proxies)


    @seq_task(2)
    def index(self):
        self.client.get("/", proxies=proxies)          


    @seq_task(3)
    def index2(self):
        path = "/user/" + self.login_id
        self.client.get(path, proxies=proxies)          


    @seq_task(4)
    def get_post_new(self):
        response = self.client.get(url="/post-new", proxies=proxies)

        content = response.content
        self.response_date_to_create_post = re.search(r'name=\"date\" value=\"(.*?)\"', str(content)).group(1)
        self.response_code_to_create_post = re.search(r'name=\"code\" value=\"(.*?)\"', str(content)).group(1)


    @seq_task(5)
    def post_post_new(self):
        self.client.post(url="/post-new", headers={"Content-Type": "application/x-www-form-urlencoded"}, 
                        data="date=" + self.response_date_to_create_post + "&code=" + self.response_code_to_create_post + "&text=Lorem+ipsum+from+Ola", 
                        proxies=proxies)



class WebsiteUser01Marek(HttpLocust):
    task_set = User01Marek
    wait_time = between(0.48, 0.50)
    trust_env=True


class WebsiteUser02Tadek(HttpLocust):
    task_set = User02Tadeusz
    wait_time = between(0.48, 0.50)
    trust_env=True

class WebsiteUser03UniqueAleksandra(HttpLocust):
    task_set = User03UniqueAleksandra
    wait_time = between(0.48, 0.50)
    trust_env=True
