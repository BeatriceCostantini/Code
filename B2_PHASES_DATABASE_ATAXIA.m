
%% DATABASE
clear all
clc

folder_path="C:\Users\b.costantini\Desktop\LAB\DATI\DATI_FINALI\PHASES_DATABASE_ATAXIA"; 

file_list=dir(fullfile(folder_path,'*.csv'));

table_Database=cell(1,numel(file_list));

for i=1:numel(file_list)
    file_name=fullfile(file_list(i).folder,file_list(i).name);
    table_Database{i}=readtable(file_name,'ReadVariableNames',false);
end

Database=[];

for i=1:numel(table_Database)
    Database=[Database;table_Database{i}];
end

writetable(Database, 'PHASES_DATABASE_ATAXIA.csv');
header={'ID','TRIAL','Patology','Phases','R_RF_PERC','R_VL_PERC','R_VM_PERC','R_G_PERC','R_BFCL_PERC','R_TA_PERC','R_PL_PERC','R_SO_PERC','R_GL_PERC','R_GMA_PERC'};
fileID=fopen('PHASES_DATABASE_ATAXIA.csv','r');
data=fread(fileID,'*char');
fclose(fileID);
fileID=fopen('PHASES_DATABASE_ATAXIA.csv','w');
fprintf(fileID, '%s\n', strjoin(header, ','));
fprintf(fileID, '%s', data);
fclose(fileID);

