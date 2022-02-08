from math import sqrt
from random import randint
from sklearn.cluster import KMeans
import pygame

def distance(p1,p2):
	return sqrt(pow(p1[0]-p2[0],2)+pow(p1[1]-p2[1],2))

pygame.init()  #Khởi tạo

screen = pygame.display.set_mode((1200,700))  #Tạo màn hình 1200x700

pygame.display.set_caption("kmeans visualization") # Tên chương trình

running = True

clock = pygame.time.Clock()

BACKGROUND = (214, 214, 214)
BLACK=(0,0,0)    #MÀU VIỀN HCN
BACKGROUND_PANEL=(249,255,230)
White=(255,255,255)

RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
PURPLE=(147,153,35)
SKY=(0,255,255)
ORANGE=(255,125,25)
GRAPE=(100,25,125)
GRASS=(55,155,65)

COLORS=[RED,GREEN,BLUE,YELLOW,PURPLE,SKY,ORANGE,GRAPE,GRASS]

font=pygame.font.SysFont('sans',40)
small_font=pygame.font.SysFont('sans',20)
textplus=font.render('+',True,White)
textminus=font.render('-',True,White)
text_run=font.render("Run",True,White)
text_random=font.render("Random",True,White)
text_algorithm=font.render("Algorithm",True,White)
text_reset=font.render("Reset",True,White)

K=0
error=0
points=[]
clusters=[]
labels=[]

while running:
	clock.tick(60)    #fps 60 lần/s
	screen.fill(BACKGROUND) # Tạo màu nền là màu biến BACKGROUND
	mouse_x, mouse_y = pygame.mouse.get_pos()  # Lấy tọa độ của chuột
	# Drawn interface
	# Drawn panel
	pygame.draw.rect(screen,BLACK,(50,50,700,500))  #(50,50) là tọa độ 700 và 500 là chiều dài dóng từ tọa độ đó tạo thành hình chữ nhật
	pygame.draw.rect(screen, BACKGROUND_PANEL, (55, 55, 690, 490))  #Tạo thêm 1 cái trong hcn đó thành viền

	# K button +
	pygame.draw.rect(screen,BLACK,(850,50,50,50))
	screen.blit(textplus,(860,50))
	# K button -
	pygame.draw.rect(screen, BLACK, (950, 50, 50, 50))
	screen.blit(textminus, (970, 50))
	# K value
	text_k=font.render("K="+str(K),True,BLACK)
	screen.blit(text_k,(1050,50))
	# Run button
	pygame.draw.rect(screen, BLACK, (850, 150, 150, 50))
	screen.blit(text_run, (860, 150))
	# Random button
	pygame.draw.rect(screen, BLACK, (850, 250, 150, 50))
	screen.blit(text_random, (860, 250))

	#Drawn mouse position when mousse is in panel  Giá trị mouse x,y phải trừ đi 50 thì mới hiển thị tọa độ min(0,0)
	if 50<mouse_x<750 and 50<mouse_y<550:
		text_mouse= small_font.render("("+str(mouse_x-50)+","+str(mouse_y-50)+")",True,BLACK)
		screen.blit(text_mouse,(mouse_x+10,mouse_y)) # mousex+10 để cho khi hiển thị k bị đè lên con chuột
	# Algorithm button
	pygame.draw.rect(screen, BLACK, (850, 450, 150, 50))
	screen.blit(text_algorithm, (860, 450))
	# Reset button
	pygame.draw.rect(screen, BLACK, (850, 550, 150, 50))
	screen.blit(text_reset, (860, 550))
	# End drawn interface

	for event in pygame.event.get():
		if event.type == pygame.QUIT:   #Nút tắt
			running = False
		if event.type==pygame.MOUSEBUTTONDOWN:
			#Creat point on panel
			if 50<mouse_x<750 and 50<mouse_y<550:
				labels=[]    #khi tạo điểm mới xóa hết label để k bị lỗi
				point=[mouse_x-50,mouse_y-50]
				points.append(point)
			# Change K Button +
			if 850<mouse_x<900 and 50<mouse_y<100:  #Vùng của nút +
				K+=1
				if K==10:
					K=0
			if 950 < mouse_x < 1000 and 50 < mouse_y < 100:  # Vùng của nút -
				K-=1
				if K==-1:
					K=9
			if 850<mouse_x<1000 and 150<mouse_y<200:  #Vùng của nút Run
				labels=[]   #reset label mỗi lần nhấn
				if clusters==[]:   # Loại bỏ lỗi k có cluster nhưng nhấn run
					continue
				# Gán những điểm vào những cluster vào những điểm gần nhất
				for p in points:
					distances_to_cluster =[]
					for c in clusters:
						distances_to_cluster.append(distance(p,c))
					min_distance=min(distances_to_cluster)
					label=distances_to_cluster.index(min_distance)  #thêm nhãn là index của cluster vào labels
					labels.append(label)
				#update cluster
				for i in range(K):
					sumx=0
					sumy=0
					count=0
					for j in range(len(points)):
						if labels[j]==i:      #Tính tổng x và y
							sumx+=points[j][0]
							sumy+=points[j][1]
							count+=1
					if count==0:  #Pass khi chia cho 0
						pass
					else:
						new_cluster_x=sumx/count
						new_cluster_y=sumy/count
						clusters[i]= [new_cluster_x,new_cluster_y]
				print("Pressed Run")
			if 850<mouse_x<1000 and 250<mouse_y<300:  #Vùng của nút Random
				labels=[]
				clusters=[]
				for i in range(K):
					random_point=[randint(0,700),randint(0,500)]
					clusters.append(random_point)
			if 850<mouse_x<1000 and 450<mouse_y<500:  #Vùng của nút Algorithm
				if K==0:   #Có thể dùng try except
					continue
				kmeans = KMeans(n_clusters=K).fit(points)  #train model tự động radom tự động run để tìm cái fit nhất
				labels=kmeans.predict(points)
				clusters=kmeans.cluster_centers_
				print("Pressed Algorithm")
			if 850<mouse_x<1000 and 550<mouse_y<600:  #Vùng của nút Reset
				labels=[]
				clusters=[]
				points=[]
				K=0
				error=0
				print("Pressed Reset")
	#Draw cluster
	for i in range(len(clusters)):
		pygame.draw.circle(screen,COLORS[i],(clusters[i][0]+50,clusters[i][1]+50),8)
	#Draw point
	for i in range(len(points)):
		pygame.draw.circle(screen,BLACK,(points[i][0]+50,points[i][1]+50),5)  #Vẽ các chấm tròn
		if labels==[]:
			pygame.draw.circle(screen, White, (points[i][0] + 50, points[i][1] + 50), 4) # Thêm chấm nhỏ màu trắng
		else:
			pygame.draw.circle(screen, COLORS[labels[i]], (points[i][0] + 50, points[i][1] + 50), 4) # Thêm chấm nhỏ màu trắng

	#Calculate and draw error
	# Error=
	error=0
	if clusters != [] and labels!= []:
		for i in range(len(points)):
			error+=round(distance(points[i],clusters[labels[i]]),2)
	text_error = font.render("Error=" + str(error), True, BLACK)
	screen.blit(text_error, (850, 350))

	pygame.display.flip()  #Phải có thì ctr mới có hiệu lực

pygame.quit()
#Đang học đến Guide 11