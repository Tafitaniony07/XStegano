import kivy
import kivymd
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager,Screen
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.boxlayout import BoxLayout,MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton,MDTextButton
from kivymd.uix.list import OneLineListItem
from kivymd.uix.bottomsheet import MDGridBottomSheet
from plyer import filechooser
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from Crypto.Hash import SHA256
import sqlite3
import os
from stegano import lsb
import pathlib
from pathlib import Path 

import re
from Fonctions.fichier import DecodeLSBF, encodeLSBF
from Fonctions.image_image import encode_image, recupere_image

from Fonctions.message import decodeLSB, encodeLSB
Window.size = (680, 580)

class SplashScreen(Screen):
    pass
class LoginScreen(Screen):
    pass
class SignupScreen(Screen):
    pass
class PassforgetScreen(Screen):
    pass
class HomeScreen(Screen):
    pass
class Message_secretScreen(Screen):
    pass
class Message_recupererScreen(Screen):
    pass
class FilencryptionScreen(Screen):
    pass
class FiledecryptionScreen(Screen):
    pass

class CipherScreen(Screen):
    pass
class View1Screen(Screen):
    pass
class View2Screen(Screen):
    pass
class View_fichierScreen(Screen):
    pass
class View_imageScreen(Screen):
    pass

class EncodageScreen(Screen):
    pass
class DecodageScreen(Screen):
    pass
class Image_encodeScreen(Screen):
    pass
class Image_decodeScreen(Screen):
    pass
class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
class Jofama(MDApp):
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.set_toolbar_font_name)
        Clock.schedule_once(self.set_toolbar_font_size)
    
    def build(self):
        global sm
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name = 'splash'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name = 'home'))
        sm.add_widget(EncodageScreen(name = 'encodage'))
        sm.add_widget(DecodageScreen(name = 'decodage'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(PassforgetScreen(name = 'pass_forget'))
        sm.add_widget(Message_secretScreen(name='message_cachee'))
        sm.add_widget(FilencryptionScreen(name='filencryption'))
        sm.add_widget(Message_recupererScreen(name='message_clair'))
        sm.add_widget(FiledecryptionScreen(name='filedecryption'))
        sm.add_widget(View1Screen(name = 'view1'))
        sm.add_widget(View2Screen(name = 'view2'))
        sm.add_widget(View_fichierScreen(name = 'view_fichier'))
        sm.add_widget(Image_encodeScreen(name="image_encode"))
        sm.add_widget(Image_decodeScreen(name="image_decode"))
        self.screen = Builder.load_file('main.kv')
        return self.screen

    def on_start(self):
        Clock.schedule_once(self.splash, 10)
        try:
            conn = sqlite3.connect('./Data_Base/registration.db')

            cur = conn.cursor()
            sql = '''CREATE TABLE  IF NOT EXISTS users (
                          email TEXT PRIMARY KEY,
                          password TEXT NOT NULL,
                          username TEXT NOT NULL
                   );'''

            cur.execute(sql)
            conn.commit()
        finally:

            cur.close()
            conn.close()
    def splash(self,*args):
        self.root.current = 'login'
    
    def connexion(self,*args):
        try:
            connection = sqlite3.connect('./Data_Base/registration.db')
            cursor = connection.cursor()
            ls = self.root.get_screen('login')
            email = ls.ids.email_input.text
            password = ls.ids.password_input.text
            hash_ob = SHA256.new(password.encode('utf-8'))
            pwd = hash_ob.digest()
            if email == "" and password == "":
                self.root.current = 'login'
                check_string = " Champs Vide ! "
                self.dialog = MDDialog( text = check_string,
                                        radius=[20, 7, 20, 7],
                                        size_hint = (0.5, 0.3),
                                        buttons =   [
                                            MDFlatButton(
                                                text="Ok",
                                                theme_text_color="Custom",
                                                text_color=self.theme_cls.primary_color,
                                                on_press = self.close_dialog,
                                                )]
                                            )
                self.dialog.open()
            else:
                cursor.execute("SELECT email, password FROM users WHERE email=?",(email,))
                result = cursor.fetchall()
                email2 = ""
                password2 = ""
                for res in result:
                    email2 = res[0]
                    password2 = res[1]
                if email == email2 and pwd != password2 :
                    check_string = "Oups! Votre mot de passe incorrect!"
                    self.dialog = MDDialog(text = check_string,
                                                    radius=[20, 7, 20, 7],
                                                    size_hint = (0.5, 0.3),
                                                    buttons =   [
                                                            MDFlatButton(
                                                                text="Réessayer",
                                                                theme_text_color="Custom",
                                                                text_color=self.theme_cls.primary_color,
                                                                on_press = self.close_dialog,
                                                                )]
                                                            )
                  
                    self.dialog.open()
                elif email == email2 and pwd == password2 and email!= "" and password!="":
                    self.root.current = 'home'
                else:
                    check_string = "Oups! Ce Compte n'existe pas\n\nVeuillez réessayer"
                    self.dialog = MDDialog(text = check_string,
                                                    radius=[20, 7, 20, 7],
                                                    size_hint = (0.5, 0.3),
                                                    buttons =   [
                                                            MDFlatButton(
                                                                text="Réessayer",
                                                                theme_text_color="Custom",
                                                                text_color=self.theme_cls.primary_color,
                                                                on_press = self.close_dialog,
                                                                )]
                                                            )
                    self.dialog.open()
            connection.commit()
        finally:
            connection.close()
    def inscription(self, *args):
        try:
            connection = sqlite3.connect('./Data_Base/registration.db')
            cursor = connection.cursor()
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            ss = self.root.get_screen('signup')
            email = ss.ids.email1_input.text
            password = ss.ids.password1_input.text
            username = ss.ids.username_input.text
            if email!="" and password!="" and username!="":
                hash_ob = SHA256.new(password.encode('utf-8'))
                hkey = hash_ob.digest()
                if(re.search(regex,email)):
                    cursor.execute("INSERT INTO users VALUES (?, ?, ?)",(email, hkey,username))
                    check_string = "\nCompte a été créé avec succès!"
                    self.dialog = MDDialog( text = check_string,
                                          radius=[20, 7, 20, 7],
                                          size_hint = (0.5, 0.3),
                                          buttons =   [
                                                MDFlatButton(
                                                    text="Fermer",
                                                    theme_text_color="Custom",
                                                    text_color=self.theme_cls.primary_color,
                                                    on_press = self.close_dialog2,
                                                    )])
                    self.dialog.open()
                else:
                    check_string = "Adresse email inconnue"
                    self.dialog = MDDialog(text = check_string,
                                        size_hint = (0.5, 0.3),
                                        radius=[20, 7, 20, 7],
                                        buttons =   [
                                            MDFlatButton(
                                                text="Réessayer",
                                                theme_text_color="Custom",
                                                text_color=self.theme_cls.primary_color,
                                                on_press = self.close_dialog,
                                                )])
                    self.dialog.open()
            else:
                check_string = "Veuillez saisir votre information"
                self.dialog = MDDialog(text = check_string,
                                    radius=[20, 7, 20, 7],
                                    size_hint = (0.5, 0.3),
                                    buttons =   [
                                        MDFlatButton(
                                            text="Réessayer",
                                            theme_text_color="Custom",
                                            text_color=self.theme_cls.primary_color,
                                            on_press = self.close_dialog,
                                            )])
                self.dialog.open()
            connection.commit()
        except:
            check_string = "[color=#FF0000]Oups! Le compte deja existe ![/color]"
            self.dialog = MDDialog( text = check_string,
                                    radius=[20, 7, 20, 7],
                                    size_hint = (0.5, 0.3),
                                    buttons =   [
                                        MDFlatButton(
                                            text="Réessayer",
                                            theme_text_color="Custom",
                                            text_color=self.theme_cls.primary_color,
                                            on_press = self.close_dialog,
                                            )])
            self.dialog.open()
        finally:
            connection.close()
    def close_dialog2(self,*args):
        ss = self.root.get_screen('signup')
        ss.ids.email1_input.text=""
        ss.ids.password1_input.text=""
        ss.ids.username_input.text=""
        self.dialog.dismiss()
    def close_dialogp(self,*args):
        cp = self.root.get_screen('pass_forget')
        cp.ids.new_password.text=""           
        cp.ids.new_email.text=""
        self.dialog.dismiss()
    def change_pass(self,*args):
       
        try:
            cp = self.root.get_screen('pass_forget')
            password = cp.ids.new_password.text           
            email= cp.ids.new_email.text
            connection = sqlite3.connect('./Data_Base/registration.db')
            cursor = connection.cursor()
            cursor.execute("SELECT email, password FROM users WHERE email=?",(email,))
            result = cursor.fetchall()
            connection.commit()  
            email2 = ""
            password2 = ""
            for res in result:
                email2 = res[0]
                password2 = res[1]
            if  email!="" and password!="" : 
                hash_ob = SHA256.new(password.encode('utf-8'))
                hkey = hash_ob.digest()
                if email==email2:
                    cursor.execute("UPDATE users SET password=? WHERE email=?",(hkey,email))
                    check_string = "\nLe mot de passe a été changé avec succès"
                    self.dialog = MDDialog(text = check_string,
                                            radius=[20, 7, 20, 7],
                                            size_hint = (0.5, 0.3),
                                            buttons =   [
                                                MDFlatButton(
                                                    text="Ok",
                                                    theme_text_color="Custom",
                                                    text_color=self.theme_cls.primary_color,
                                                    on_press = self.close_dialogp,
                                                    )])
                    self.dialog.open()

                    connection.commit()
                    
                else:
                    self.dialog = MDDialog(text = "Ce Compte n'existe pas!",
                                            radius=[20, 7, 20, 7],
                                            size_hint = (0.5, 0.3),
                                            buttons =   [
                                                MDFlatButton(
                                                    text="Ok",
                                                    theme_text_color="Custom",
                                                    text_color=self.theme_cls.primary_color,
                                                    on_press = self.close_dialog,
                                                    )])
                    self.dialog.open() 
            else:
                self.dialog = MDDialog(text = "Champs incompletes!!",
                                        radius=[20, 7, 20, 7],
                                        size_hint = (0.5, 0.3),
                                        buttons =   [
                                            MDFlatButton(
                                                text="Ok",
                                                theme_text_color="Custom",
                                                text_color=self.theme_cls.primary_color,
                                                on_press = self.close_dialog,
                                                )])
                self.dialog.open()  

        finally:
            connection.close()
    def encode_msg(self):
        msg_enc = self.root.get_screen('message_cachee')
        image = msg_enc.ids.img_in.text
        cover_image = msg_enc.ids.img_cover.text
        message = msg_enc.ids.msg_in.text
        if image!="" and cover_image!="" and len(message)!="":
            encodeLSB(message,image,cover_image)
            Content="Message dissimulé"
            self.dialog = MDDialog( title="Succès",text = Content,
                                    size_hint = (0.5, 0.3),
                                    radius=[20, 7, 20, 7],
                                    buttons =   [
                                            MDFlatButton(
                                                text="Fermer",
                                                theme_text_color="Custom",
                                                text_color=self.theme_cls.primary_color,
                                                on_press = self.close_dialog,
                                                )])
            self.dialog.open()
        elif image=="":
            Content="Importer une image de couverture "
            self.dialog = MDDialog( title="Succès",text = Content,
                                    size_hint = (0.5, 0.3),
                                    radius=[20, 7, 20, 7],
                                    buttons =   [
                                            MDFlatButton(
                                                text="Fermer",
                                                theme_text_color="Custom",
                                                text_color=self.theme_cls.primary_color,
                                                on_press = self.close_dialog,
                                                )])
            self.dialog.open()
        else:
            Content="saisir le message "
            self.dialog = MDDialog( title="Succès",text = Content,
                                    size_hint = (0.5, 0.3),
                                    radius=[20, 7, 20, 7],
                                    buttons =   [
                                            MDFlatButton(
                                                text="Fermer",
                                                theme_text_color="Custom",
                                                text_color=self.theme_cls.primary_color,
                                                on_press = self.close_dialog,
                                                )])
            self.dialog.open()
    def decode_msg(self):
        msg_dec = self.root.get_screen('message_clair')
        view = self.root.get_screen('view1')
        stego_medium = msg_dec.ids.img_dec.text
        if stego_medium!="":
            message_clair = decodeLSB(stego_medium)
            msg_dec.ids.msg_out.text = message_clair
        else:
            Content="Inserer l'image contenant le message"
            self.dialog = MDDialog( title="Succès",text = Content,
                                    size_hint = (0.5, 0.3),
                                    radius=[20, 7, 20, 7],
                                    buttons =   [
                                            MDFlatButton(
                                                text="Fermer",
                                                theme_text_color="Custom",
                                                text_color=self.theme_cls.primary_color,
                                                on_press = self.close_dialog,
                                                )])
            self.dialog.open()

    
    def encrypt_file(self):
        fs = self.root.get_screen('filencryption')
        file_to_hide = fs.ids.file_in.text
        new_name = fs.ids.img_cover.text
        image = fs.ids.img_in.text
        file = pathlib.Path(file_to_hide)
        if file.suffix==".txt":
            if file_to_hide!="" and image!="":
                cachee = encodeLSBF(file_to_hide,image,new_name)
                Content = "L'insertion du fichier a été réussie !"
                self.dialog = MDDialog( text = Content,
                                        radius=[20, 7, 20, 7],
                                        size_hint = (0.5, 0.3),
                                        buttons =   [
                                            MDFlatButton(
                                                text="OK",
                                                theme_text_color="Custom",
                                                text_color=self.theme_cls.primary_color,
                                                on_press = self.close_dialog,
                                                )])
                self.dialog.open()
            elif file_to_hide!="" and image=="":
                Content = "Insérer une image de couverture"
                self.dialog = MDDialog( text = Content,
                                        radius=[20, 7, 20, 7],
                                        size_hint = (0.5, 0.3),
                                        buttons =   [
                                            MDFlatButton(
                                                text="Réessayer",
                                                theme_text_color="Custom",
                                                text_color=self.theme_cls.primary_color,
                                                on_press = self.close_dialog,
                                                )])
                self.dialog.open()
            else:
                Content = "Insérer le fichier à cacher"
                self.dialog = MDDialog( text = Content,
                                        radius=[20, 7, 20, 7],
                                        size_hint = (0.5, 0.3),
                                        buttons =   [
                                            MDFlatButton(
                                                text="Réessayer",
                                                theme_text_color="Custom",
                                                text_color=self.theme_cls.primary_color,
                                                on_press = self.close_dialog,
                                                )])
                self.dialog.open()
        else:
            Content = file.name+"inconnue"
            self.dialog = MDDialog( text = Content,
                                    radius=[20, 7, 20, 7],
                                    size_hint = (0.5, 0.3),
                                    buttons =   [
                                        MDFlatButton(
                                            text="Réessayer",
                                            theme_text_color="Custom",
                                            text_color=self.theme_cls.primary_color,
                                            on_press = self.close_dialog,
                                            )])
            self.dialog.open()
    def decrypt_file(self):
        fsd = self.root.get_screen('filedecryption')
        finalFilename = fsd.ids.new_name.text
        file_image = fsd.ids.img_d.text 
        if file_image!="":   
            DecodeLSBF(file_image,finalFilename)
            Content = "La répération du fichier a été bien deroulée"
            self.dialog = MDDialog( text = Content,
                                    radius=[20, 7, 20, 7],
                                    size_hint = (0.5, 0.3),
                                    buttons =   [
                                        MDFlatButton(
                                            text="OK",
                                            theme_text_color="Custom",
                                            text_color=self.theme_cls.primary_color,
                                            on_press = self.close_dialog,
                                            )])
            self.dialog.open()
        else:
            Content = "Aucune image selectionée"
            self.dialog = MDDialog( text = Content,
                                    radius=[20, 7, 20, 7],
                                    size_hint = (0.5, 0.3),
                                    buttons =   [
                                        MDFlatButton(
                                            text="Réessayer",
                                            theme_text_color="Custom",
                                            text_color=self.theme_cls.primary_color,
                                            on_press = self.close_dialog,
                                            )])
            self.dialog.open()

    
    def save_image(self):
        img = self.root.get_screen('image_encode')
        image_visible = img.ids.image_1.text
        image_visible_aucune = img.ids.vide.text
        image_visible_aucune1 = img.ids.vide1.text
        image_cache = img.ids.img_2.text
        img_ext_vi = pathlib.Path(image_visible)
        img_ext_ca = pathlib.Path(image_cache)
        stego = img.ids.img_stg.text        

        if image_visible!="" and image_cache!="" and stego!="":   
            
            cachee=open(image_cache) #image cachée
            couverture=open(image_visible)#image encore visible 
            if img_ext_vi.suffix==img_ext_ca.suffix and cachee.size==couverture.size:

                encode_image(image_visible,image_cache,stego)

                Content = " Image fusionée!"
                self.dialog = MDDialog(text = Content,
                                                radius=[20, 7, 20, 7],
                                                 size_hint = (0.5, 1),
                                                buttons =   [
                                                    MDFlatButton(
                                                        text="Fermer",
                                                        theme_text_color="Custom",
                                                        text_color=self.theme_cls.primary_color,
                                                        on_press = self.close_dialog,
                                                        )])
                self.dialog.open()
                    
            else:
                Content=img_ext_vi.name + " et " + img_ext_ca.name + " ne sont pas identiques"
                self.dialog = MDDialog(text = Content,
                                        radius=[20, 7, 20, 7],
                                        buttons =   [
                                                        MDFlatButton(
                                                            text="Fermer",
                                                            theme_text_color="Custom",
                                                            text_color=self.theme_cls.primary_color,
                                                            on_press = self.close_dialog,
                                                            )])
                self.dialog.open()
        else :
            image_visible_aucune = image_visible
            image_visible_aucune1 = image_cache

    #Extraire l'image cachee
    def extraire_image(self):
        img_d= self.root.get_screen('image_decode')
        name = img_d.ids.new_name.text
        stego = img_d.ids.img_d.text
        vide = img_d.ids.vided.text
        if stego == "":
            stego = vide
            check_string = "Insérer l'image fusioné"
            self.dialog = MDDialog(text = check_string,
                                radius=[20, 7, 20, 7],
                                size_hint = (0.5, 1),
                                buttons =   [
                                        MDFlatButton(
                                            text="Fermer",
                                            theme_text_color="Custom",
                                            text_color=self.theme_cls.primary_color,
                                            on_press = self.close_dialog,
                                            )])
            self.dialog.open()
        else:
            recupere_image(stego,name)
            check_string = "Image recupérée avec succès"
            self.dialog = MDDialog(text = check_string,
                                radius=[20, 7, 20, 7],
                                size_hint = (0.5, 1),
                                buttons =   [
                                        MDFlatButton(
                                            text="Fermer",
                                            theme_text_color="Custom",
                                            text_color=self.theme_cls.primary_color,
                                            on_press = self.close_dialog,
                                            )])
            self.dialog.open()

    def set_toolbar_font_name(self, *args):
        tool1 = self.root.get_screen('home')
        tool3 = self.root.get_screen('encodage')
        tool4 = self.root.get_screen('decodage')
        tool1.ids.toolbar.ids.label_title.font_name = "./Fonts/dollie.ttf"
        tool1.ids.appbar.ids.label_title.font_name = "./Fonts/dollie.ttf"
        tool3.ids.tool_enc.ids.label_title.font_name = "./Fonts/dollie.ttf"
        tool4.ids.tool_dec.ids.label_title.font_name = "./Fonts/dollie.ttf"
    def set_toolbar_font_size(self, *args):
        tool1 = self.root.get_screen('home')
        tool3 = self.root.get_screen('encodage')
        tool4 = self.root.get_screen('decodage')
        tool1.ids.toolbar.ids.label_title.font_size = '35sp'
        tool1.ids.appbar.ids.label_title.font_size = "32sp"
        tool3.ids.tool_enc.ids.label_title.font_size = '35sp'
        tool4.ids.tool_dec.ids.label_title.font_size = '35sp'
    def actual(self,*args):
        actual_one = self.root.get_screen('message_cachee')
        actual_one.ids.msg_in.text=""
        actual_one.ids.img_in.text=""
        actual_one.ids.img_cover.text=""
        actual_one.ids.long_msg.text = ""
        actual_two = self.root.get_screen('message_clair')
        actual_two.ids.img_dec.text=""
        actual_two.ids.img_cov_dec.source=""
        actual_two.ids.msg_out.text=""
        fsd = self.root.get_screen('filedecryption')
        fsd.ids.new_name.text = ""
        fsd.ids.img_d.text = ""
        fsd.ids.img_cov_src.source = ""
        fs = self.root.get_screen('filencryption')
        fs.ids.file_in.text = ""
        fs.ids.img_cover.text = ""
        fs.ids.img_in.text = ""
        
        actual_seven = self.root.get_screen('image_encode')
        actual_seven.ids.image_1.text=""
        actual_seven.ids.img_2.text=""
        actual_seven.ids.img_stg.text=""
        actual_8= self.root.get_screen('image_decode')
        actual_8.ids.img_deco.text=""
        actual_8.ids.new_name.text=""
        actual_8.ids.img_d.text=""
        actual_8.ids.img_deco.source=""
    def close_dialog(self,*args):
        self.dialog.dismiss()
    def section_exit(self, *args):
        self.root.current = 'home'
    def exit(self, *args):
        self.root.current = 'home'
    def image_select(self):
        filechooser.open_file(on_selection = self.Image)
    def Image(self,s_image):
        msg_enc = self.root.get_screen('message_cachee')
        msg_dec = self.root.get_screen('message_clair')
        fs = self.root.get_screen('filencryption')
        fsd = self.root.get_screen('filedecryption')
        msg_dec.ids.vide.text = ""
        msg_enc.ids.vide.text=""
        fs.ids.vide.text=""
        fsd.ids.vide.text=""
        if s_image :
            msg_enc.ids.img_in.text = s_image[0]
            msg_enc.ids.img_in.source = s_image[0]
            msg_dec.ids.img_dec.text = s_image[0]
            msg_dec.ids.img_cov_dec.source = s_image[0]
            fs.ids.img_in.text = s_image[0]
            fs.ids.img_in.source = s_image[0]
            fsd.ids.img_cov_src.source = s_image[0]
            fsd.ids.img_d.text = s_image[0]
         

    def file_select(self):
        filechooser.open_file(on_selection = self.File)
    def File(self, choose):
        fs = self.root.get_screen('filencryption')
        fs.ids.vide_file.text=""
        if choose:
            fs.ids.file_in.text = choose[0]

    #Transition Page
    def decryption_msg(self):
        self.root.current = "message_clair"
    def decryption_file(self):
        self.root.current = "filedecryption"
    def encryption_msg(self):
        self.root.current = "message_cachee"
    def encryption_image(self):
        self.root.current = "image_encode"
    def decryption_image(self):
        self.root.current = "image_decode"
    def encryption_file(self):
        self.root.current = "filencryption"
    def section_page(self):
        self.root.current = 'section'
    def Encodage(self):
        self.root.current = 'encodage'
    def Decodage(self):
        self.root.current = 'decodage'
    def apropos(self,*args):
        info = "ShyPhy\nAuteur : Joseph Jofama\nContact : jensen@yahoo.fr\nType: Securite"
        self.dialog = MDDialog(title = "A propos", text = info,
                              size_hint = (0.5, 0.4),
                              radius=[20, 7, 20, 7],
                              buttons =   [
                                            MDFlatButton(
                                                text="Fermer",
                                                theme_text_color="Custom",
                                                text_color=self.theme_cls.primary_color,
                                                on_press = self.close_dialog,
                                                )])
        self.dialog.open()


    def image_visible(self):
            filechooser.open_file(on_selection = self.Image_one)
    def Image_one(self,image):
        img_1 = self.root.get_screen('image_encode')
        img_1.ids.vide.text=""
        if image :
            img_1.ids.image_1.text = image[0]
    def image_cachee(self):
            filechooser.open_file(on_selection = self.Image_two)
    def Image_two(self,image):
        img_1 = self.root.get_screen('image_encode')
        img_1.ids.vide1.text=""
        if image:
            img_1.ids.img_2.text = image[0]
    def image_fusionee(self):
            filechooser.open_file(on_selection = self.Image_three)
    def Image_three(self,image):
        img_d = self.root.get_screen('image_decode')
        img_d.ids.vided.text=""
        if image:
            img_d.ids.img_d.text = image[0]
            img_d.ids.img_deco.source = image[0]
    def returne(self,*args):
        self.root.current = 'encodage'
    def annuler(self,*args):
        self.root.current = 'home'

    def close_view1(self,*args):
        self.root.current = 'message_clair'
        view = self.root.get_screen('view1')
        view.ids.view1_txt.text = ""
    
    def close_view_image(self,*args):
        self.root.current = 'message_cachee'
        view = self.root.get_screen('view_image')
        view.ids.v_image.source=""
    def close_view_fichier(self,*args):
        self.root.current = 'filencryption'
        view = self.root.get_screen('view_fichier')
        view.ids.v_fichier.source=""
    def exit_home(self,*args):
        self.root.current="login"
        ls = self.root.get_screen('login')
        ls.ids.email_input.text = ""
        ls.ids.password_input.text = ""
        self.dialog.dismiss()
    def view1_image(self):
        self.root.current = 'view1'

    def voir_image(self):
        self.root.current = 'view_image'
        mc = self.root.get_screen('message_cachee')
        image = self.root.get_screen('view_image')
        image.ids.v_image.source = mc.ids.img_in.source
    def voir_fichier(self):
        self.root.current = 'view_fichier'
        f = self.root.get_screen('filencryption')
        image = self.root.get_screen('view_fichier')
        image.ids.v_fichier.source = f.ids.img_in.source

    def quitter(self,*args):
        self.dialog = MDDialog(text = "Vous voulez quitter?",
                              size_hint = (0.5, 1),
                              radius=[20, 7, 20, 7],
                              buttons =   [
                                            MDFlatButton(
                                                text="Non",
                                                theme_text_color="Custom",
                                                text_color=self.theme_cls.primary_color,
                                                on_press = self.close_dialog,
                                                ),
                                             MDFlatButton(
                                                text="Oui",
                                                theme_text_color="Custom",
                                                text_color=self.theme_cls.primary_color,
                                                on_press = self.exit_home,
                                                )])
        self.dialog.open()
  
import sys
sys.path.append("./Fonctions")
from fichier import *
from message import *
from image_image import*

if __name__ ==  "__main__":
    Jofama().run()
