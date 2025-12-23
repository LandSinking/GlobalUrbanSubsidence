
clc
clear

xlsx_path = ".\Fig3_data.xlsx";
table_data = readtable(xlsx_path, "Sheet", "Region", "VariableNamingRule","preserve");



figure('Position', [100, -100, 1000, 1200]);  


num_rows = 4;
num_cols = 3;

hspace = 0.10;  

subplot_w = (1 - (num_cols + 1) * hspace) / num_cols;


left_positions = zeros(1, num_cols);
for col = 1:num_cols
    left_positions(col) = hspace + (col-1) * (subplot_w + hspace);
end


% ==============================
for r = 1:10
    
    region_name = table_data.Region{r};
   

    decc_f_ratio = table_data.Deceleration_ratio(r);
    acce_f_ratio = table_data.Acceleration_ratio(r);
    

    decc_f_median = abs(table_data.Deceleration_median(r));
    acce_f_median = abs(table_data.Acceleration_median(r));


    decc_Q1 = abs(table_data.Deceleration_Q1(r));
    decc_Q3 = abs(table_data.Deceleration_Q3(r));
    acce_Q1 = table_data.Acceleration_Q1(r);
    acce_Q3 = table_data.Acceleration_Q3(r);


    decc_err_low_0  = abs(decc_f_median - decc_Q1);
    decc_err_high_0 = abs(decc_Q3 - decc_f_median);
    acce_err_low_0  = abs(acce_f_median - acce_Q1);
    acce_err_high_0 = abs(acce_Q3 - acce_f_median);


    ax = subplot(num_rows, num_cols, r);

    row_idx = ceil(r / num_cols);
    col_idx = mod(r-1, num_cols) + 1;


    old_pos = get(ax, 'Position');

    new_pos = [ left_positions(col_idx), old_pos(2), subplot_w, old_pos(4) ];
    set(ax, 'Position', new_pos);
 


    hold on; box on;
    set(gca, 'FontName', 'Arial');


    % ------------------------
    % ------------------------
    yyaxis left
    bar(1, decc_f_ratio, 'FaceColor',[81/255,118/255,162/255], 'EdgeColor','none');
    bar(2, acce_f_ratio, 'FaceColor',[151/255,67/255,88/255], 'EdgeColor','none');

    ylim([0 0.3]);
    yticks(0:0.1:0.3);
    yticklabels({'0','10','20','30'});
    set(gca, 'FontSize',16,'FontWeight','bold');
    set(gca, 'TickLength',[0.02 0.025]);

    set(gca, 'XTick', []);
    xticklabels([]);

    if mod(r-1, num_cols) == 0
        ylabel('Proportion (%)', 'FontName','Arial','FontSize',24,'FontWeight','bold');
    else
        set(gca, 'YTickLabel', []);
    end

    set(gca,'YColor','k','FontSize',18);

    h = title(region_name, 'FontWeight','bold','FontName','Arial','FontSize',24);
    pos = get(h,'Position');
    set(h,'Position',[pos(1), pos(2)+0.01, pos(3)]);


    % ------------------------
    % ------------------------
    yyaxis right


    ylim([-22 30]);
    yticks(0:10:30);
    yticklabels({'0','10','20','30'});

    scatter(1, decc_f_median, 26*abs(decc_f_median), 'filled', ...
        'MarkerFaceColor',[81/255,118/255,162/255]);
    scatter(2, acce_f_median, 26*abs(acce_f_median), 'filled', ...
        'MarkerFaceColor',[151/255,67/255,88/255]);

    decc_color = [81/255,118/255,162/255];
    acce_color = [151/255,67/255,88/255];

    errorbar(1, decc_f_median, decc_err_low_0, decc_err_high_0, ...
        'Color',decc_color,'LineWidth',1.2,'CapSize',10);

    errorbar(2, acce_f_median, acce_err_low_0, acce_err_high_0, ...
        'Color',acce_color,'LineWidth',1.2,'CapSize',10);


    if (row_idx <= 3 && col_idx == num_cols) || (row_idx == 4 && col_idx == 1)
        ylabel('Magnitude (mm/yr)','FontName','Arial','FontSize',24,'FontWeight','bold');
    else
        set(gca,'YTickLabel',[]);
    end

    set(gca,'YColor','k','FontSize',18);
end

print('.\fig3_c_plot', '-dpng', '-r600'); 


