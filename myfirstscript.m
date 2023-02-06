clc
clear all

% My First Script
disp("Go in the direction of your dreams, live the life you have imagined")
fprintf("\n")

% fprintf to print any thing of to write any text.
% \n for new line

% lets create a matrix with random integers
% 
% myMat=randi(3,3)
% transpose(myMat)
% myMattranspose= myMat'
% double click on the command, right click and help. Which will open a
% popup, which has all the detials of the function, with example.

% --------------------------------------------------------------------
disp("# Some random matrices(20)")
fprintf("\n")

% myzeros= zeros(20,30);
% myones = ones(10,10);
% myrndomints= randi(5,6);
% In a matrix eg rand(2,1) the 1st value= rows, 2nd value= column.
% if me want to make a random 3x3 matrix then
% disp("1. when rand is used while forming any matrices, it will generate any random varibale  with decimals, fractions and integers ")
% a= rand(3,3)
% % Make a 3x3 matrix with random integers.
% disp("2. when randi is used while forming any matrices, it will generate any matrix with integers")
% b= randi(3,3)% (row,column).
% ----------------------------------------------------------------

disp("# Matrix Multiplication(35)")
fprintf("\n")

% Matrix has two types of matrix multiplication,
% 1. Row by column multiplication
% 2. Element by Element Multiplication
% disp("1. Row by column Multiplication")
% M1 = [-1,6;2,4]
% M2= [3,-2;9,5]
% M= M1*M2
% disp("2. Element by Element Multiplication")
% m1 = [-1,6;2,4]
% m2= [3,-2;9,5]
% m= m1.*m2
% % For division also same thing
% ElementDivision=m1./m2
% --------------------------------------------------------------
% IF Statement
disp("# If Statement(53)")
fprintf("\n")
 
% number= input("Please enter your number: ");
%  
% if number < 0
%     disp("Please add Positive Number only") 
% elseif(number > 0) && (number <=100)
%     disp("you're perfect")
% else 
%     disp("enter any number between 0 to 100 only")
% end
%------------------------------------------------------------
% Switch Statement
% while writing an action in command window add ' '.
disp("# Switch Statment(68)")
fprintf("\n")

% 
% n= input('Enter a number: ');
% m= input('Enter another number: ');
% 
% action = input('What calculation should I perform? ');
% % 
% switch action
%     case 'add'
%         output = n+m
%     case 'substract'
%         output = n-m
%     case 'multiply'
%         output = n*m
%     case 'division'
%         output = n/m
%     otherwise
%         disp("Sorry, Alay I can't do that...")
% end
%-------------------------------------------------------
% For loop
disp("# For Loop(91)")
fprintf("\n")
% 
% % if we write i= 1:10 or 1:1:10, then it calls, i= 1 to 10 in steps of 1.
% % if we write i= 1:10 or 1:2:10, then it calls, i= 1 to 10 in steps of 2.
% 
% fprintf("eg:1, 1:1:10\n")
% for i = 1:10
%     disp(i)
% end
% 
% 
% fprintf("eg:2, 1:2:10\n")
% for j= 1:2:10
%     disp(j)
% end
% 
% 
% fprintf("eg:3\n")
% disp("- Step giving externally")
% fprintf('\n')
% % If we want to give external steps, as in n numbers, or rows and columns
% 
% n= 100;
% step= 10;
% for k = 0 : step:n
%     disp(k)
% end
% 
% 
% fprintf("eg:3, row and column *\n")
% rows=3;
% columns=5;
% for i=1:rows
%     for j=1:columns
%         fprintf('*')
%     end
%     fprintf('\n')
% end
% ----------------------------------------------------

disp("# While loop(132)")
fprintf("\n")
% fprintf("eg:1,\n")
% 
% value = 50;
% gap = 5;
% while value>0
%     value=value-gap;
%     disp(value)
% end


% fprintf("eg:2, Current of Heater wire\n")
% 
% possiblecurrent = 8;
% 
% while true
%     input = randi(10);
%     if input >= possiblecurrent
%         disp("Over limit, SHUT DOWN!")
%         fprintf("--\n\n")
%         break
%     end
%     disp("Every thing is OKAY!")
%     fprintf("-\n\n")
% end
% -------------------------------------------------------
fprintf("# Create your own fucntion(159)\n\n")

% To create your own fucntion 
% 1. From New select Function, That will create a new file with function,

% 2. Now for example we want to create a function which will calculate a 
% hypotenuse of triangle using Pythagoras theorem, 

% 3. In that file edit the code accordingly as shown below, and save  

% function[C] = Pythagoras(A,B)
% %Function calculate using pythagoras
% %   Side^2 + Side^2 = Hypotenuse^2
% C= sqrt((A^2)+(B^2));
% end

% 4. After saving whenever, we want to do Pythagoras of triangle,with any side, 
% suppose 3,4 we have to write
% Pythagoras(3,4)

% --------------------------------------------------------------
fprintf("# To read a data of different file(180)\n\n")

%---------------------------------------------------------------
fprintf("# Preallocate some memory(183)\n\n")
% this will check the performance of the MATLAB
% disp("eg:1 Check Performance")
% 
% tic
% m= zeros(1,1000000);
% for i= 1:1000000
%     m(i)= i;
% end
% toc

%----------------------------------------------------------------

fprintf("# Creating basic plots(196)\n\n")
% myData = csvread('try.csv');

x= [1,2,3,4;5,6,7,8;9,0,1,2;3,4,5,6];
% y= [2,3,4,5;6,7,8,9;0,1,2,3;4,5,6,7];
% X=sin(45);
% Y=sin(30);
% figure(1)
% plot(x,y)
% grid on
% axis tight % this will fit the window of figure exactly from top to bottom of the window border or figure.

% a= 0:pi/100:2*pi;
% b= sin(a);
% c= tan(b);
% plot(a,b,'oB')% here oB means, it will form a figure in shape o and color B= Blue;
% hold on
% plot (b,a,'--m')% here --m means, it will form a figure in form of -- with color magneta;
% plot (c,b,'^g')
% xlabel('pi value')
% ylabel('trigo')
% title("My first plot")
% legend('ab','ba','cb')
% grid on
% axis tight

% ---------------------------------------------------------------
fprintf("# Working with Images(223) \n\n")
% myim=imread("Myphoto.JPG");
% figure(2)
% image(myim)
% grid on
% GridAlphaMode = 'auto';
% grid on 
% imshow(myim)% this will open another pop for the image with a original aspect ratio of image. 
fprintf("(Keep checking help for knowing more for any specific function we learned till now.)\n")
% % there many other option for the image, to crop, to change its size and
% % pixels and even more, please check its help section to know more

% -----------------------------------------------------------------------

fprintf("# Creating 3D plots.\n\n")
% create soem 3d data and plot it

% % Eg: 1.
% fprintf("1. Mesh Plot\n")
% Mesh Creates Wireframe
%   A). Plot points from 1 D grid 
% %a.
% figure(1)
% peaks(2)

% %b.
% z = peaks(5);
% figure(2)
% mesh(z)

% %c.
% n=-1:0.25:1;% this will create a number line from -1 to 1 in the gap of 0.25
% figure(3)
% Z=peaks(n)
% surf(Z)% surf creates a 3D surface plot.

%   B). Plot poiints from 2 D gird

x=-2:0.5:2;  % -2 to 2 with gap of 0.5
y=1:0.2:2;   % 1 to 2 with gap of 0.2
[x,y]=meshgrid(x,y);
figure(4)
% z= peaks(x,y);
surf(peaks(x,y))


% fprintf("Other Examples.\n\n")

% x = -2*pi:.5:2*pi;
% 
% [X,Y]=ndgrid(x); % mesh grid is the type of grid 
% Z= sin(X)+cos(Y); % peaks()
% figure(4)
% surf(X, Y, Z)
% title("Graph1: Ndgrid")
% colorbar
% figure(5)
% 
% [A,B]= meshgrid(x);
% C= sin(A)+cos(B);
% meshc(A,B,C)
% title("Graph 2: Meshgrid")
% colorbar






