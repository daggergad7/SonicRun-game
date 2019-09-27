import pygame
pygame.init()
win = pygame.display.set_mode((800,400))
pygame.display.set_caption('Side Scroller')
ff=''
def text1(word,x,y):
    font = pygame.font.SysFont(None, 25)
    text = font.render("{}".format(word), True, (255,0,0))
    return win.blit(text,(x,y))


def inpt():
    word=""
    text1("Please enter your name and press Enter key: ",30,30) #example asking name
    pygame.display.flip()
    done = True
    while done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                done=False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    word+=str(chr(event.key))
                if event.key == pygame.K_b:
                    word+=chr(event.key)
                if event.key == pygame.K_c:
                    word+=chr(event.key)
                if event.key == pygame.K_d:
                    word+=chr(event.key)

                if event.key == pygame.K_e:
                    word+=str(chr(event.key))
                if event.key == pygame.K_f:
                    word+=chr(event.key)
                if event.key == pygame.K_g:
                    word+=chr(event.key)
                if event.key == pygame.K_h:
                    word+=chr(event.key)

                if event.key == pygame.K_i:
                    word+=str(chr(event.key))
                if event.key == pygame.K_j:
                    word+=chr(event.key)
                if event.key == pygame.K_k:
                    word+=chr(event.key)
                if event.key == pygame.K_l:
                    word+=chr(event.key)

                if event.key == pygame.K_m:
                    word+=str(chr(event.key))
                if event.key == pygame.K_n:
                    word+=chr(event.key)
                if event.key == pygame.K_o:
                    word+=chr(event.key)
                if event.key == pygame.K_p:
                    word+=chr(event.key)

                if event.key == pygame.K_q:
                    word+=str(chr(event.key))
                if event.key == pygame.K_r:
                    word+=chr(event.key)
                if event.key == pygame.K_s:
                    word+=chr(event.key)
                if event.key == pygame.K_t:
                    word+=chr(event.key)
                if event.key == pygame.K_u:
                    word+=str(chr(event.key))
                if event.key == pygame.K_v:
                    word+=chr(event.key)
                if event.key == pygame.K_w:
                    word+=chr(event.key)
                if event.key == pygame.K_x:
                    word+=chr(event.key)

                if event.key == pygame.K_y:
                    word+=str(chr(event.key))
                if event.key == pygame.K_z:
                    word+=chr(event.key)

                if event.key == pygame.K_RETURN:
                    done=False


    return word
