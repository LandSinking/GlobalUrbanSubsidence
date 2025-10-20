clc
clear

data = readtable(".\Fig3_data.xlsx", "Sheet", "Region", "VariableNamingRule","preserve");

figure('Position', [100, -100, 800, 1200]); 
num_rows = 4;
num_cols = 3;

for r = 1:10
    region_name = data.Region{r};

    decc_ratio = data.Deceleration_ratio(r);
    acce_ratio = data.Acceleration_ratio(r);

    decc_median = data.Deceleration_median(r);
    acce_median = data.Acceleration_median(r);
    
    subplot(num_rows, num_cols, r);
    hold on;
    
    set(gca, 'FontName', 'Arial');
    bar(1, decc_ratio, 'FaceColor', [81/255, 118/255, 162/255], 'EdgeColor', 'none'); 
    bar(2, acce_ratio, 'FaceColor', [151/255, 67/255, 88/255], 'EdgeColor', 'none'); 
   
    scatter(1, decc_ratio + 0.05, 20 * abs(decc_median), 'filled', 'MarkerFaceColor', [81/255, 118/255, 162/255]); 
    scatter(2, acce_ratio + 0.05, 20 * abs(acce_median), 'filled', 'MarkerFaceColor', [151/255, 67/255, 88/255]); 

    ylim([0 0.3]);
    yticks(0:0.1:0.3);  

    yticklabels({'0', '10', '20', '30'});  


    set(gca, 'FontName', 'Arial', 'FontSize', 12,'FontWeight', 'bold');
    set(gca, 'TickLength', [0.02 0.025]); 
    
    set(gca, 'XTick', []);
    xticklabels([]);
    
    h = title(region_name, 'FontWeight', 'bold', 'FontName', 'Arial', 'FontSize', 16);
    pos = get(h, 'Position');
    set(h, 'Position', [pos(1), pos(2) + 0.01, pos(3)]);

    if mod(r-1, num_cols) == 0  
        ylabel('Proportion (%)', 'FontName', 'Arial', 'FontSize', 14, 'FontWeight', 'bold');
    else
        set(gca, 'YTickLabel', []);
    end
   
end

print('.\Fig3_c_plot.tif', '-dtiff', '-r600'); 


