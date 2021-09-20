import pygame, os, random, sys, Static

os.chdir(os.path.dirname(sys.argv[0]))

pygame.init() # initiate pygame
 
SIZE = (1920, 1080) #screen size
screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN) # set screen

pygame.display.set_caption("Stonks") #screen name

clock = pygame.time.Clock() #define clock

def drawWindows(List, x, y):
    for i in List:
        if i[2] == 0:
            color = (229, 226, 63)
        else:
            color = (0,0,0)
        pygame.draw.rect(screen, color, [x+5+i[0]*15, 1080-y+5+i[1]*25, 10, 20])

player = Static.Bird()

Static.makeTowers()

tick = 0
# -------- Main Program Loop -----------
while True:
    if player.alive == True and Static.gameOver == False:
        if Static.started == True:
            tick += 1
            if tick == 100:
                if random.randint(0,2) > 0:
                    Static.opPlanes.append(Static.OpPlane())
                tick = 0
                Static.score += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePosition = event.pos

            if Static.gameOver == True:
                if replay.collidepoint(mousePosition):
                    Static.started = False
                    Static.gameOver = False
                    player.alive = True
                    Static.score = 0
                    player.set()
                    Static.opPlanes.clear()
                    Static.towers.clear()
                    Static.makeTowers()
                elif quit.collidepoint(mousePosition):
                    pygame.quit()
                elif reset.collidepoint(mousePosition):
                    Static.highscore = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if player.alive == True:
                    player.jump()
                    Static.started = True

    screen.fill(Static.SKY_COLOR) #background

    if Static.gameOver == False:

        obsticleBlocks = []
        for t in Static.towers:
            if Static.started == True:
                t.move()
                obsticleBlocks.append([pygame.draw.rect(screen, (150,150,150), [int(round(t.x)), 1080-t.y, 100, t.y]), t])
                drawWindows(t.windows, t.x, t.y)

        player.move()
        playerBlock = pygame.draw.rect(screen, Static.SKY_COLOR, [player.x-40, int(round(player.y)), 96, 48], 1)
        screen.blit(pygame.transform.rotate(Static.plane, player.rot), (player.x-48, int(round(player.y))-48))
        
        for op in Static.opPlanes:
            if op.move() == "terminate":
                Static.opPlanes.remove(op)
            obsticleBlocks.append([screen.blit(pygame.transform.rotate(Static.opPlane, op.rot), (op.x, int(round(op.y)))), op])
        
        for o in obsticleBlocks:
            if playerBlock.colliderect(o[0]):
                if o[1].type == "plane":
                    o[1].alive = False
                    if player.alive == True:
                        Static.deathMessage = "Death caused by colliding with another flying plane"
                if o[1].type == "building":
                    if player.alive == True:
                        Static.deathMessage = "Death caused by flying into a building"
                player.alive = False

        screen.blit(Static.font30.render(f"{Static.score}", False, (250,250,250)),(10, 10))
    
    else:
        screen.blit(Static.font200.render("Game Over", False, (250,250,250)),(350, 10))
        screen.blit(Static.font50.render(f"{Static.deathMessage}", False, (250,250,250)),(100, 300))
        screen.blit(Static.font50.render(f"Score: {Static.score}", False, (250,250,250)),(100, 370))
        screen.blit(Static.font50.render(f"Highscore: {Static.highscore}", False, (250,250,250)),(100, 440))

        replay = pygame.draw.rect(screen, (250,250,250), [700, 800, 540, 50])
        screen.blit(Static.font30.render("Replay", False, (50,50,50)),(920, 800))

        reset = pygame.draw.rect(screen, (250,250,250), [700, 875, 540, 50])
        screen.blit(Static.font30.render("Reset", False, (50,50,50)),(920, 875))

        quit = pygame.draw.rect(screen, (250,250,250), [700, 950, 540, 50])
        screen.blit(Static.font30.render("Quit", False, (50,50,50)),(920, 950))

    pygame.display.flip()
 
    clock.tick(60) #fps
 
pygame.quit()