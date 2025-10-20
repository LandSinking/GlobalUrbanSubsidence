
clc
clear

filePth = ".\Houston";
saveDir = ".\Houston";

icity = "Houston";    

load(fullfile(filePth, 'dates.mat'), 'remainDate');
dates_datetime = datetime(remainDate,'InputFormat','yyyyMMdd');
dates_datenum = datenum(dates_datetime);
ts = geotiffread(fullfile(filePth, 'timeseries_clipped.tif'));
[row,col,~] = size(ts);

change_point_datetime = NaT(row, col);  
change_point_datetime.Format = 'yyyy-MM-dd';
change_point_type = nan(row,col);    
% parameters of linear fit for all dates
change_point_par_k0 = nan(row,col);
change_point_par_b0 = nan(row,col);    
% parameters of linear fit for dates before the change point
change_point_par_k1 = nan(row,col);
change_point_par_b1 = nan(row,col);   
% parameters of linear fit for dates after the change point
change_point_par_k2 = nan(row,col);
change_point_par_b2 = nan(row,col);    

if isempty(gcp('nocreate'))
    parpool;
end
 
disp(strcat(icity, " begin to process! "));
t1 = tic();

N = row;
parfor_progress(N);

parfor m = 1:row
    for n = 1:col
        y = squeeze(ts(m, n, :)); 
        y = y - y(1);  
        y=y*1000; % unit in mm, m to mm
        x0 = dates_datenum - dates_datenum(1) + 1;
        x = x0/365.25;

        x_datenum = dates_datenum;
        x_datetime = dates_datetime;
         
    
        if sum(abs(y))==0
            vel(m,n)=nan;
            continue;
        end              
        len = length(y);           
        
        %% simple linear fit
        [b0,bint0,r0,rint0,stats0] = regress(y,[x ones(length(y),1)]);
        rss_sl = sum(r0.^2);

        change_point_par_k0(m,n) = b0(1);
        change_point_par_b0(m,n) = b0(2);            
        change_point_par_RSSsl(m,n) = rss_sl;
       

        %% piecewise linear fit
        before_b_all=nan(len,2);
        after_b_all=nan(len,2);
        RSS_all=nan(len,1);
      
        counter=1;
      
        for k = 2:len-1
            before_g = y(1:k);
            after_g = y(k:end);
                
            [b1,bint1,r1,rint1,stats1] = regress(before_g,[x(1:k) ones(length(before_g),1)]);
            [b2,bint2,r2,rint2,stats2] = regress(after_g,[x(k:end) ones(length(after_g),1)]);
    
            rss = sum(r1.^2) + sum(r2.^2);
            counter = counter + 1;        
            before_b_all(counter,:)=b1';
            after_b_all(counter,:)=b2';
            RSS_all(counter)=rss;
        end        
        [~,indmin] = min(RSS_all);   
        before_b=before_b_all(indmin,:);
        before_b=before_b';        
        after_b=after_b_all(indmin,:);
        after_b=after_b';            
        breakpoint_datetime = x_datetime(indmin); % datetime
        change_point_datetime(m,n)=breakpoint_datetime;        
        change_point_par_k1(m, n) = before_b(1);
        change_point_par_b1(m, n) = before_b(2); 
        change_point_par_k2(m, n) = after_b(1);
        change_point_par_b2(m, n) = after_b(2);
       

    end
    parfor_progress;
end
parfor_progress(0);
disp(strcat(icity, " has been finished! "));
save(strcat(saveDir, '\',icity, '_piecewise.mat'), ...
    'change_point_datetime',  ...       
    'change_point_par_k0', 'change_point_par_b0',...
    'change_point_par_k1', 'change_point_par_b1', ...
    'change_point_par_k2', 'change_point_par_b2');

disp(strcat(icity, "'s result has been saved!")); 
toc(t1);




    
