''' 15 Puzzle or Slide Puzzle - Features: OOP - Multithread functions - error handling
'''
try:
    import pygame
    from pygame.locals import *
    from pygame.sprite import *
    import random
    import sys
    import threading
    
except ImportError as err:
    print(err)
    pygame.quit()
    sys.exit()
    

DEBUG=False

WHITE=(255,255,255)
BLACK =(0,0,0) 

#list img tiles
idl =["0.png","1.jpg","2.jpg","3.jpg","4.jpg","5.jpg","6.jpg","7.jpg","8.jpg","9.jpg","10.jpg","11.jpg","12.jpg","13.jpg","14.jpg","15.jpg"]
sel_idl=["0s.png","1s.jpg","2s.jpg","3s.jpg","4s.jpg","5s.jpg","6s.jpg","7s.jpg","8s.jpg","9s.jpg","10s.jpg","11s.jpg","12s.jpg","13s.jpg","14s.jpg","15s.jpg"]


#BOARD Attributes
COL=4
ROW=4
SQUARE_LEN=50

if DEBUG:
    idt=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,0,15] #FOR DEBUG
else:
    idt=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]    



#window attributes
WIDTH = 200
HEIGHT = 200



class Tile(Sprite):
    def __init__(self,idl,idt,rect):
        Sprite.__init__(self)
        
        self.idt=idt
        self.can_move_to=''
        
        if not DEBUG:
            n=self.get_random(self.idt)
        
        if DEBUG:
            n=self.get_and_remove(self.idt)
        try:
            self.image = pygame.image.load(idl[n])

        except pygame.error as err:
            
            print(err)
            pygame.quit()
            sys.exit()
            

        self.id = n
        self.rect= self.image.get_rect()
        self.rect.left,self.rect.top=rect
        
        
        
        self.selected=False
        


    def is_selected(self):
        return self.selected
            

    def select(self):
        self.selected=True     

    def deselect(self):
        self.selected=False

    def slide_to(self,move):
       
        if move=='dx' and move==self.can_move_to:
            
            self.rect.left+=SQUARE_LEN
            return 0
            
        elif move=='sx' and move==self.can_move_to:
           
            self.rect.left-=SQUARE_LEN
            return 0

        elif move=='up' and move==self.can_move_to:
            
            self.rect.top-=SQUARE_LEN
            return 0
        elif move=='down' and move==self.can_move_to:
            
            self.rect.top+=SQUARE_LEN
            return 0
        else:
            return -1
        

    def change_img(self,imglist1,imglist2):
        
        try:
            if self.selected:
                self.image=pygame.image.load(imglist2[self.id]) 
            
            else:
                self.image=pygame.image.load(imglist1[self.id])

        except pygame.error as err:

            print(err)
            pygame.quit()
            sys.exit()

    def get_id(self):
        return self.id
   
    def get_pos(self):
        return self.rect.left,self.rect.top

    def set_pos(self,pos):
        self.rect.left,self.rect.top=pos
    
    def __str__(self):
        return "Tile num: " + str(self.id) + " Can move to: " + str(self.can_move_to)

    def get_random(self,lista):

        elem=random.choice(lista)
        temp=elem
        lista.remove(elem)   
        return temp

    def get_and_remove(self,lista):
        
        elem = lista[0]
        temp=elem
        lista.remove(elem)
        return temp
    
        
            
class Game():
    def __init__(self,idl,sel_idl):

        self.mosse= 0
        self.win=False
        self.clicked=False
        
        self.not_valid_key=''
        
        self.move=''

        #coords list
        self.coords_win=[(150, 150), (0, 0), (50, 0), (100, 0), (150, 0), (0, 50), (50, 50), (100, 50), (150, 50), (0, 100), (50, 100), (100, 100), (150, 100), (0, 150), (50, 150), (100, 150)]
        self.coords_last=[]
        

        #sprite lists
        self.tiles = pygame.sprite.Group()
        self.selectable_tiles=pygame.sprite.Group()
        self.selected_tile=pygame.sprite.GroupSingle()

        #create board
        self.create_board()
                
    def create_board(self):
        for row in range(ROW):
            for col in range(COL):
                rect=(col*SQUARE_LEN,row*SQUARE_LEN)
                
                self.tiles.add(Tile(idl,idt,rect))

    #VERIFY IF MOUSE COLLIDES A TILE
    def mouse_collide_tile(self,mouse_pos):

        for t in self.selectable_tiles:

            
            if t.rect.collidepoint(mouse_pos):
                print("Clicked " + str(t))
                if t.is_selected():
                    self.clicked=False
                    t.deselect()
                    self.selected_tile.empty()
                else:
                    self.clicked=True

                    #Deselect selected tiles

                    for st in self.selectable_tiles:
                        st.deselect()

                        
                    t.select()
                    
                    self.selected_tile.add(t)
        
    #EVENTS PROCESSING    
    def process_events(self):
        
        for event in pygame.event.get():

            #Sys exit
            if event.type == pygame.QUIT:
                
                return True
                
                    
                    

            #CLICK SX MOUSE
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:   
                mouse_pos= pygame.mouse.get_pos()

                if not self.win:

                    self.mouse_collide_tile(mouse_pos)
                
                    
                else:
                    
                    return True
                    
                    
                        
                    

            
            elif event.type == pygame.KEYDOWN and event.key ==K_LEFT:
                if self.clicked:
                    #print("Freccia sx premuta")
                    self.move='sx'
                    self.clicked=False 
                    
                    


                        
            elif event.type == pygame.KEYDOWN and event.key ==K_RIGHT:
                if self.clicked:
                    #print("Freccia dx premuta")
                    self.move='dx'
                    self.clicked=False
                    
                    


                        
            elif event.type == pygame.KEYDOWN and event.key ==K_UP:
                if self.clicked:
                    #print("Freccia su premuta")
                    self.move='up'
                    self.clicked=False
                    
                    


                      
            elif event.type == pygame.KEYDOWN and event.key ==K_DOWN:
                if self.clicked:

                    #print("Freccia giù premuta")
                    self.move='down'
                    self.clicked=False
                    
                    

            return False

    #increments number of moves    
    def mosse_increment(self):
        self.mosse+=1
        pygame.display.set_caption("Moves: "+ str(self.mosse))
    
   
    def set_void_pos(self,pos):
        for t in self.tiles:
            if t.get_id()==0:
                t.set_pos(pos)

    def verify_win(self):
        i=0
        while i<=15:
            for t in self.tiles:
                if t.get_id()==i:
                    self.coords_last.append(t.get_pos())
                    i+=1
        #print(self.coords_last)

    def run_logic(self):

        threads = []        
    
        
        self.verify_win()

        
        
            

        if self.coords_last==self.coords_win:
            self.win=True
            
        else:
            
            self.coords_last=[]
            
            
             
        if not self.win:        
        
            
            self.selectable_tiles.empty()
            void_pos=self.get_void_pos()
            #print(void_pos)

            self.selected_tile_move()
                    
    
            #Multithreading - search for selectable tiles  
            
            for i in range(10):#10 threads
                tr= threading.Thread(target=self.search_selectable_tiles, args=(void_pos,))
                tr.start()
                threads.append(tr)



            for t in self.tiles:
                t.change_img(idl,sel_idl)

    
    def selected_tile_move(self):
        for t in self.selected_tile:
                        
            
            if self.move=='sx':
                old_pos=t.get_pos()
                
                res=t.slide_to('sx')
                t.deselect()
                if res==0:
                    
                    self.mosse_increment()
                    self.set_void_pos(old_pos)
                    
                else:
                    #print("mossa illegale!")
                    pygame.display.set_caption("Illegal move")
                
                
            elif self.move=='dx':
                old_pos=t.get_pos()
                res=t.slide_to('dx')
                t.deselect()
                if res==0:
                    
                    self.mosse_increment()
                    self.set_void_pos(old_pos)
                    
                else:
                    #print("mossa illegale!")
                    pygame.display.set_caption("Illegal move")
                
            elif self.move=='up':
                old_pos=t.get_pos()
                res=t.slide_to('up')
                t.deselect()
                if res==0:
                    
                    self.mosse_increment()
                    self.set_void_pos(old_pos)
                    
                else:
                    
                    #print("mossa illegale!")
                    pygame.display.set_caption("Illegal move")
                
            elif self.move=='down':
                old_pos=t.get_pos()
                res=t.slide_to('down')
                t.deselect()
                if res==0:
                    
                    self.mosse_increment()
                    self.set_void_pos(old_pos)
                    
                else:
                    #print("mossa illegale!")
                    pygame.display.set_caption("Illegal move")

            self.move=''
    
    def search_selectable_tiles(self,void_pos):

        for t in self.tiles:
                result=self.is_next_void(void_pos,t.get_pos())
                if result != '':
                    t.can_move_to=result
                    #print(t,result)
                    self.selectable_tiles.add(t)

    def get_void_pos(self):
        
        for elem in self.tiles:
            if elem.get_id()==0:
                #print(elem.get_pos())
                return elem.get_pos()
    
    def display_frame(self, screen):
        screen.fill(BLACK)

        if self.win:


            font = pygame.font.SysFont("Trebuchet MS", 18)
            text = font.render("You won! - Click to exit", True, WHITE)
            center_x = (WIDTH / 2) - (text.get_width() / 2)
            center_y = (HEIGHT / 2) - (text.get_height() / 2)
            screen.blit(text, [center_x, center_y])

            #pygame.display.set_caption("YOU WON! ")
            pygame.display.flip()
            
        if not self.win:
            
            self.tiles.draw(screen)

            #update display      
            
        
            pygame.display.flip()

    #Se la tessera è prossima alla casella vuota, la funzione ritorna dove si trova la casella vuota rispetto la tessera
    def is_next_void(self,pos1,pos2):
    
    
        if pos1[0]+50==pos2[0] and pos1[1]==pos2[1]:
            
            return 'sx'
        elif pos1[0]-50==pos2[0] and pos1[1]==pos2[1]:
            return 'dx'
        elif pos1[0]==pos2[0] and pos1[1]+50==pos2[1]:
            return 'up'
        elif pos1[0]==pos2[0] and pos1[1]-50==pos2[1]:
            
            return 'down'
        else:
            return ''


def main():

    

    #inizializzazione pygame
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    pygame.display.set_caption("15!")
    pygame.display.set_icon(pygame.image.load("icon.jpg"))

    done=False

    #inizializzazione clock
    clock = pygame.time.Clock()

    #inizializzazione game instance
    game=Game(idl,sel_idl)


    while not done:

        done = game.process_events()

        game.run_logic()

        game.display_frame(screen)

        clock.tick(30)
            
            
    #uscita dal gioco
    pygame.quit()
    sys.exit()
    


main()
