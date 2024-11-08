clc
clear
close all

%
max_time = 2400;




filename = "200s_5V_2400.xlsx";
% Чтение файла в виде таблицы
% Чтение файла с пропуском первой строки
data = readmatrix(filename, 'NumHeaderLines', 1);

% Извлечение столбцов
time_our = data(:, 1);
current = data(:, 2);
filt_current_our = movmean(medfilt1(current, 3), 3);

%
% plot(time_our, filt_current_our);

%

filename = "2400s_5V_pir.txt";
% Чтение файла в виде таблицы
% Чтение файла с пропуском первой строки
data = readmatrix(filename, 'NumHeaderLines', 20);

% Извлечение столбцов
% time_fabric = data(:, 1);
freq = 2e3;
dt = 1/freq;
time_fabric = 0:dt:max_time;
time_fabric = time_fabric(2:end);
current = data(:, 2);
filt_current_fabric = movmean(medfilt1(current, 3), 3);
%
% plot(time_fabric', filt_current_fabric);


%
freq = 2e3;
dt = 1/freq;
max_time = 2400;
time_new = 0:0.2:2400;

fabric_pirani = interp1(time_our, filt_current_our, time_new);
our_pirani = interp1(time_fabric, filt_current_fabric, time_new);
%
% plot(time_new, fabric_pirani, time_new,our_pirani)
%
% plot(our_pirani, fabric_pirani)

%
max_ind = length(time_new);
cut_ind = floor(max_ind/5);
ind = (max_ind - cut_ind: max_ind);
plot(time_new(ind), normalize_vec(fabric_pirani(ind)), time_new(ind),normalize_vec(our_pirani(ind)))

%%

plot(time_new(ind), normalize_vec(fabric_pirani(ind)), 'LineWidth', 5);
hold on;
plot(time_new(ind), normalize_vec(our_pirani(ind)), 'LineWidth', 5);
hold off;

% Подписи к осям
xlabel('Время', 'FontSize', 24);
ylabel('Вакуум от 0.1 до 3 Па', 'FontSize', 24);

% Сетка
grid on;

% Увеличение шрифта
set(gca, 'FontSize', 24);

% Легенда
legend('Наш', 'Фабричный', 'FontSize', 24);
%%
freq = 2e3;
dt = 1/freq;
max_time = 2400;
time_new = 0:0.2:2400;

fabric_pirani = interp1(time_our, filt_current_our, time_new);
our_pirani = interp1(time_fabric, filt_current_fabric, time_new);
%
% plot(time_new, fabric_pirani, time_new,our_pirani)
%
% plot(our_pirani, fabric_pirani)

%
max_ind = length(time_new);
cut_ind = floor(max_ind/5);
ind = (50/0.2: 100/0.2);
% plot(time_new(ind), normalize_vec(fabric_pirani(ind)), time_new(ind),normalize_vec(our_pirani(ind)))


plot(time_new(ind), normalize_vec(fabric_pirani(ind)), 'LineWidth', 5);
hold on;
plot(time_new(ind), normalize_vec(our_pirani(ind)), 'LineWidth', 5);
hold off;

% Подписи к осям
xlabel('Время', 'FontSize', 24);
ylabel('Вакуум от Атмосферы до 3 Па', 'FontSize', 24);

% Сетка
grid on;

% Увеличение шрифта
set(gca, 'FontSize', 24);

% Легенда
legend('Наш', 'Фабричный', 'FontSize', 24);

