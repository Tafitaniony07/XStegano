from PIL.Image import *

def encode_image(image_couverture, image_cachee, imagefinal):

    cachee=open(image_cachee) #image encore visible
    couverture=open(image_couverture) #image cachée
    (xmax,ymax)=couverture.size

    im=new('RGB',(xmax,ymax),(255,255,255))

    for j in range(ymax):
        for i in range(xmax):
            c1=Image.getpixel(cachee,(i,j))
            c2=Image.getpixel(couverture,(i,j))
            r=16*int(c1[0]/16)+int(c2[0]/16)
            v=16*int(c1[1]/16)+int(c2[1]/16)
            b=16*int(c1[2]/16)+int(c2[2]/16)
            Image.putpixel(im, (i,j), (r,v,b))
                                      
    im.save(imagefinal+'.bmp',"BMP")   
 

def recupere_image(stego_image,image_recuperee):
    imagefinal=open(stego_image) #image code
    (xmax,ymax)=imagefinal.size

    im=new('RGB',(xmax,ymax),(255,255,255))

    for j in range(ymax):
        for i in range(xmax):
            c1=Image.getpixel(imagefinal,(i,j))
            r=16*(c1[0]%16)
            v=16*(c1[1]%16)
            b=16*(c1[2]%16)
            Image.putpixel(im, (i,j), (r,v,b))
                                      
    im.save(image_recuperee+'.bmp',"BMP")