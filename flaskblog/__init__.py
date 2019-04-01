
from flask import Flask,flash,url_for
from flask_cors import CORS, cross_origin
from flask import render_template,redirect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


import pyrebase




app = Flask(__name__)



# api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = '50c5edea62ca6d87f4895446fde274c3'
config = {
    "apiKey": "AIzaSyAXZYFU8vfkVUunVMSZn9Yy2rBTUJ6n5hA",
    "authDomain": "major-6c311.firebaseapp.com",
    "databaseURL": "https://major-6c311.firebaseio.com",
    "projectId": "major-6c311",
    "storageBucket": "major-6c311.appspot.com",
    "messagingSenderId": "461731456375"
}
firebase=pyrebase.initialize_app(config)
auth1=firebase.auth()
cred1={
  "type": "service_account",
  "project_id": "major-6c311",
  "private_key_id": "42d67efa0caf4db4a2684662c34340c334dae33e",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC8THpAhTONl/LQ\n5d6QV3tgI34HSht5IpemU62CRgzOExi0E6l0yiB6/8hr7bQd5kwVO3/KkkWomZw/\nohc/RtbUxq71H0wBo3A2B+oNLDVRsLUN8Z4WBWjJJ75z8bS09qDucvlV3bhaXn/R\nmx+xvAIB8YksgzX51qWASCEHXLfc088ff7o374HEEVP5eE2sO4ZEY29bX6LDEXIr\nRd51gMJVDNHWnSAmZFC35GpxEokJo1C7wkkhUm8U+kGW4yiD0YIHVLSq++mF/ZnD\nTEIOrwp4Qh6m5QAYgCr4CbhsDDrwvE+hmB9tV2KTTCXF+Jo8ZY9aM0uqMyi81Lzb\nuDZrPabJAgMBAAECggEACkSaWwfYdJVvXIRYc2MN24N79R5Nqrif7+Y6vTKgMqGY\ndINo93EpPcPSdE45RvMevX6p3IxG56d+vXqTjXQJtX8jHcNH5AP7U7rxQKgjPTHn\nYZwGHJnNacC00kJBMigLxQz4ez30tlrWWgH9Q7YmnuACtK5wBFB35Guqf2oHLa+4\nCtO62794cJ9mdyMKX2nkDBCCaTyEjeZQG/hPeEY1/tFYxyZyLbNRIIam4G4QSlzB\nRLNZo7rcuRJVfmh1Le0ye3z0zQodNCbmc5TTXjrdUAg6NUYAK+q0MNgNmbEntUOr\nO8vDaZormzPAGO+PFrPlZLw9jFnOJw+ef2KyoNL3XQKBgQD3iqEb0gM/WQvuRlVS\nElceKPGmQVQYYSBtSUhAeVGRe5raUqDeMGaieAug4GFU429vMp14l1OqUc0Yr4W3\neK0C0C4ePkoE8GaFt0xz9El5Eks/2KZ6XEuKHxg2izP2zN0JgHAtxK75AInq+7mN\nGow3ZlCUnwVcoCwaerPIKczijQKBgQDCu58n+MQKrjmFrnG5pd83T2R/0i8V8sah\nHOo6CFAxy+ZdRWXEoLGZs60P50P2/1suNGADYAkoqPRZix9dbJvTrQcn1zzhUuju\nFRzWkd1amyrOJptmKyy5F4iWFEuMqCbxf0PCNheXKMBhrHQYF1+q0rpGiWzn+BIF\nUoP0g1YkLQKBgDQGsOG1+/S+dGF56si7DhBKrq8wn8oX78bIViUm2lvnTJ6CK0lH\nhuqyrE79mbdLrcoDK1GDDJSJaL+9dC8hb8tdkbPNh6UOGZ4U7j6YozCNBb+/ew3Q\nhBfdfStJinxehj5O/kTAR74RvOrkSRU89SdXm6wA2BGloF9YVpzFHEipAoGBAJhX\n/ghgZsZQTPIXaiMp8DouI1qYTXvnRZuvqlKiRFLgyKT5cMdmS+sKFP9XFuW6GlRI\nZ0Dcte2YWClhXLVTDYmJWQrDKX7BxTbVT41R6hFDSTakH3jLmB5pmdKHqB8vQeA2\nhwT+GnCIUhFXwC9EwfQ7Db23L3s+qKJ/TnpQ8Wg1AoGAP6zqdqDS2lFB4Smhenfg\nIlcrP9A0KufjDe+cvU67rJ27bAv49fDCpT/pmmmj/5Mc5sTO6uq8XiHJ/kbUnsUE\nsqi7AwIU9DQjPN4QAodEVjUIzgXxvP9vS2tKKZwTi4IawbmXV88muyVkl4Y857MJ\nA/HH2dL/P4/gAPCnlKBHdCM=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-x3g2e@major-6c311.iam.gserviceaccount.com",
  "client_id": "110792151492582632506",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-x3g2e%40major-6c311.iam.gserviceaccount.com"
}

cred = credentials.Certificate(cred1)
default_app=firebase_admin.initialize_app(cred)
from firebase_admin import auth
db = firestore.client()


bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view = 'login'
# function name of route for login_req
login_manager.login_message_category = 'info'
# function name of route for login_req


from flaskblog import routes

