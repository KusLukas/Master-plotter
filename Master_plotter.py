from numpy import delete, abs,array,linspace
import matplotlib.pyplot as plt
import massiveOES
from massiveOES import MeasuredSpectra
import glob, os
from collections import defaultdict
from json import load
from matplotlib.pyplot import cm
# from camera_formats import read_tiff
import tkinter as tk
import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory


class GI_plotter:
    def __init__(self,master):
        root.title("Master plotter")
        root.resizable(width=False, height=False)
        root.geometry('{}x{}'.format(1080, 600))

        self.basic_buttons = tk.Frame(root, relief=tk.RAISED, height=5, pady=1, borderwidth = 4)
        self.loading_jsons=tk.Frame(root, relief=tk.RAISED, height=5, pady=1, borderwidth = 4)

        btn_open = tk.Button(self.basic_buttons, text="Load dictionary", command=self.open_dict)
        btn_save = tk.Button(self.basic_buttons, text="Save As...", command=self.save_file)
        btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        btn_save.grid(row=1, column=0, sticky="ew", padx=5)
        self.basic_buttons.grid(row=0, column=3, sticky="e")

        ttk.Label(self.loading_jsons,text="Selected folder//*//oes*//*xxxxns*xxxbin*_fitted.json").grid(row=0,column=0)
        btn_open_sub = tk.Button(self.loading_jsons, text="Load jsons from subfolders", command=self.open_jsons_subfolders)
        ttk.Label(self.loading_jsons,text="Selected folder//*xxxxns*xxxbin*_fitted.json").grid(row=0,column=1)
        btn_open_main = tk.Button(self.loading_jsons, text="Load jsons from folder", command=self.open_jsons_mainfolder)
        btn_open_main.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        btn_open_sub.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.loading_jsons.grid(row=0, column=4, sticky="w")

        welcome_message="""Welcome to Master plotter. Few things to remember especially during loading of the data. Loading jsons from folder and subfolders is pretty simple, but few things need to be kept in mind. Firstly there have to be words "ns" and "bin" with numbers before them. The script is looking for theese words and takes the integers before as plotting parameters. The structure of path that is used for individual buttons and structure of required filenames is displayed at labels for appropriet button. Also the filename have to end with _fitted.json. The plotting is pretty intuitive and there shoudnt be any limitations, but keep in mind plotting of every parameter "on" can take a while. Thats all you need to know, GO PLOT THEM ALL!!!
        """
        self.textbox_wel = tk.Text(root, relief=tk.RAISED, pady=1, borderwidth = 4)
        self.textbox_wel.grid(row=1, column=4,rowspan=18, sticky="e")
        self.textbox_wel.insert(tk.END, str(welcome_message)+'\n')

        if 'myVar' in locals():
            if self.loaded==True:
                self.Buttons_and_stuff()


    def Buttons_and_stuff(self):
        self.species_buttons = tk.Frame(root, relief=tk.RAISED, height=5,width=10, pady=1, borderwidth = 4)
        self.bin_buttons = tk.Frame(root, relief=tk.RAISED, height=5,width=10, pady=1, borderwidth = 4)
        self.delay_buttons = tk.Frame(root, relief=tk.RAISED, height=5,width=10, pady=1, borderwidth = 4)
        self.plot_buttons = tk.Frame(root, relief=tk.RAISED, height=5,width=10, pady=1, borderwidth = 4)
        self.cond_buttons = tk.Frame(root, relief=tk.RAISED, height=5,width=100, pady=1, borderwidth = 4)
        self.species_buttons = tk.Frame(root, relief=tk.RAISED, height=5,width=100, pady=1, borderwidth = 4)



        for i in self.species_choice:
            self.spec_plot={i: False}
        self.check_spec=[None]*len(self.species_choice)
        for x in range(len(self.species_choice)):
            self.species_choice[x]=self.species_choice[x][:-6]
            self.check_spec[x] = ttk.Checkbutton(self.species_buttons, text=self.species_choice[x], variable=self.species_choice[x])
            self.check_spec[x].grid(row=x+1, column=0)
            self.check_spec[x].state(['!alternate'])
            if x==0:
                self.check_spec[x].state(['selected'])
            else:
                self.check_spec[x].state(['!selected'])

        for i in self.bins_choice:
            self.bin_plot={i: False}
        self.check_bins=[None]*len(self.bins_choice)
        for x in range(len(self.bins_choice)):

            self.check_bins[x] = ttk.Checkbutton(self.bin_buttons, text=self.bins_choice[x], variable=self.bins_choice[x])
            self.check_bins[x].grid(row=x+1, column=0)
            self.check_bins[x].state(['!alternate'])
            if x==0:
                self.check_bins[x].state(['selected'])
            else:
                self.check_bins[x].state(['!selected'])

        for i in self.delays_choice:
            self.delay_plot={i: False}
        self.check_dly=[None]*len(self.delays_choice)
        cl=-1
        rw=0
        for x in range(len(self.delays_choice)):
            self.check_dly[x] = ttk.Checkbutton(self.delay_buttons, text=self.delays_choice[x], variable=self.delays_choice[x])
            if x%5==0:
                cl+=1
                rw=0
            rw+=1
            self.check_dly[x].grid(row=rw, column=cl)
            self.check_dly[x].state(['!alternate'])
            if x<5:
                self.check_dly[x].state(['selected'])
            else:
                self.check_dly[x].state(['!selected'])

        ttk.Label(self.species_buttons,text="Select species").grid(row=0,column=0,sticky='w')
        tk.Button(self.species_buttons, command=self.change_all_spec,text='Change All').grid(column=1, row=int(len(self.species_choice)/2))

        ttk.Label(self.bin_buttons,text="Select bins").grid(row=0,column=0)
        tk.Button(self.bin_buttons, command=self.change_all_bins,text='Change All').grid(column=1, row=int(len(self.bins_choice)/2))

        tk.Button(self.delay_buttons, command=self.change_all_delays,text='Change All').grid(column=1, row=6)
        ttk.Label(self.delay_buttons,text="Select Delays").grid(row=0,column=0)

        ttk.Button(self.plot_buttons, command=lambda: Math_and_plot.initial_plot(self),text='Plot').grid(column=0, row=0)

        tk.Label(self.cond_buttons, text = 'Y axis limits').grid(row=0,column=0)
        self.y_low=tk.IntVar()
        self.y_high=tk.IntVar()
        tk.Entry(self.cond_buttons, textvariable = self.y_low).grid(row=0,column=1)
        self.y_low.set(300)
        tk.Entry(self.cond_buttons, textvariable = self.y_high).grid(row=0,column=2)
        self.y_high.set(1000)

        tk.Label(self.cond_buttons, text = 'Max deviation').grid(row=1,column=0)
        self.max_std=tk.IntVar()
        tk.Entry(self.cond_buttons, textvariable = self.max_std).grid(row=1,column=1)
        self.max_std.set(20)

        tk.Label(self.cond_buttons, text = 'Fontsize').grid(row=2,column=0)
        self.font=tk.IntVar()
        tk.Entry(self.cond_buttons, textvariable = self.font).grid(row=2,column=1)
        self.font.set(26)

        self.textbox = tk.Text(root, relief=tk.RAISED, pady=1, borderwidth = 4)


        self.species_buttons.grid(row=1, column=0,columnspan=5, sticky="w")
        self.bin_buttons.grid(row=2, column=0,columnspan=5, sticky="w")
        self.delay_buttons.grid(row=3, column=0,columnspan=5, sticky="w")
        self.plot_buttons.grid(row=0, column=0,columnspan=1, sticky="w")
        self.cond_buttons.grid(row=4, column=0,columnspan=4, sticky="w")
        self.textbox.grid(row=1, column=4,rowspan=18, sticky="e")


    def choices_and_checkbuttons(self):
        self.bins_choice=list(self.data_file.keys())
        delay_arr=[]
        for i in self.data_file.keys():
            for j in range(len(self.data_file[i].keys())):
                delay=list(self.data_file[i].keys())[j]
                if delay not in delay_arr:
                    delay_arr.append(list(self.data_file[i].keys())[j])
        self.delays_choice=list(delay_arr)
        species_arr=[]
        for i in self.data_file.keys():
            for j in self.data_file[i].keys():
                for k in self.data_file[i][j].keys():
                    for l in range(len(self.data_file[i][j][k].keys())):
                        specie=list(self.data_file[i][j][k].keys())[l]
                        if specie not in species_arr and 'stdrr' not in specie:
                            species_arr.append(list(self.data_file[i][j][k].keys())[l])

        self.species_choice=list(species_arr)

    def print_in_gui(self,input):
        self.textbox.insert(tk.END, str(input)+'\n')

    def print_in__welcome_gui(self,input):
        self.textbox_wel.insert(tk.END, str(input)+'\n')


    def clearTextInput(self):
        self.textbox.delete("1.0",tk.END)
    def clearTextInput_wel(self):
        self.textbox_wel.delete("1.0",tk.END)


    def Species_label_fun(self,*a):
        self.species_display.set(self.data)

    def bin_label_fun(self,*a):
        self.bins_display.set(self.bin_box.get())

    def delay_label_fun(self,*a):
        self.delays_display.set(self.delay_box.get())

    def open_dict(self):
        # """Open a file for editing."""
        filepath = askopenfilename(
            filetypes=[("Jsons", "*.json"), ("All Files", "*.*")]
        )
        # print(filepath)
        # filepath=r"D:\FIles\Work_files\work\Eindhoven_work\ratios\test_format_nested_dictionary.json"
        if not filepath:
            return
        f = open(filepath,)
        self.data_file=load(f)

        GI_plotter.choices_and_checkbuttons(self)

        self.Buttons_and_stuff()
        self.loaded=True
        return self.data_file


    def open_jsons_subfolders(self):
        """Open a file for editing."""
        path_tem = askdirectory()
        self.opening_path=path_tem+'//'+'*//'+'oes*'+'//*_fitted.json'
        GI_plotter.open_jsons(self)

    def open_jsons_mainfolder(self):
        """Open a file for editing."""
        path_tem = askdirectory()
        GI_plotter.print_in__welcome_gui(self,'Wait I am loading')
        self.opening_path=path_tem+'//*_fitted.json'
        GI_plotter.open_jsons(self)

    def open_jsons(self):
        # GI_plotter.clearTextInput_wel(self)
        print('Wait I am plotting')
        target_dict = defaultdict(dict)
        for file in glob.iglob(self.opening_path):
            # print(file)
            v=file.split('\\')
            # print(v)
            del_ld=v[-1].find('ns')
            bin_ld=v[-1].find('bin')
            # print(del_ld,bin_ld)
            del_ld_val=v[-1][del_ld-4:del_ld]
            bin_ld_val=v[-1][bin_ld-3:bin_ld]
            try:
                int(del_ld_val[0])
            except ValueError:
                del_ld_val=v[-1][del_ld-3:del_ld]
            try:
                int(del_ld_val[0])
            except ValueError:
                del_ld_val=v[-1][del_ld-2:del_ld]
            try:
                int(del_ld_val[0])
            except ValueError:
                del_ld_val=v[-1][del_ld-1:del_ld]

            try:
                int(bin_ld_val[0])
            except ValueError:
                bin_ld_val=v[-1][bin_ld-3:bin_ld]
            try:
                int(bin_ld_val[0])
            except ValueError:
                bin_ld_val=v[-1][bin_ld-2:bin_ld]
            try:
                int(bin_ld_val[0])
            except ValueError:
                bin_ld_val=v[-1][bin_ld-1:bin_ld]

            del_var=del_ld_val
            bin_var=bin_ld_val

            data = massiveOES.MeasuredSpectra.from_json(file)
            target_dict['{}'.format(bin_ld_val)]['{}'.format(del_ld_val)]={}
            sp_pos=[]
            strv_arr=[]
            strd_arr=[]
            stvv_arr=[]
            stvd_arr=[]
            ftrv_arr=[]
            ftrd_arr=[]
            ftvv_arr=[]
            ftvd_arr=[]

            print('Current position: {}bin, {}delay.'.format(bin_var,del_var))

            for specname in data.spectra:

                target_dict['{}'.format(bin_var)]['{}'.format(del_var)]['{}'.format(specname)]={}
                strv=data.spectra['{}'.format(specname)]['params'].prms['N2CB_Trot'].value
                strd=data.spectra['{}'.format(specname)]['params'].prms['N2CB_Trot'].stderr
                stvv=data.spectra['{}'.format(specname)]['params'].prms['N2CB_Tvib'].value
                stvd=data.spectra['{}'.format(specname)]['params'].prms['N2CB_Tvib'].stderr
                ftrv=data.spectra['{}'.format(specname)]['params'].prms['N2PlusBX_Trot'].value
                ftvv=data.spectra['{}'.format(specname)]['params'].prms['N2PlusBX_Tvib'].value
                ftrd=data.spectra['{}'.format(specname)]['params'].prms['N2PlusBX_Trot'].stderr
                ftvd=data.spectra['{}'.format(specname)]['params'].prms['N2PlusBX_Tvib'].stderr
                target_dict['{}'.format(bin_var)]['{}'.format(del_var)]['{}'.format(specname)]['N2CB_Trot_value'] = strv
                target_dict['{}'.format(bin_var)]['{}'.format(del_var)]['{}'.format(specname)]['N2CB_Trot_stdrr'] = strd
                target_dict['{}'.format(bin_var)]['{}'.format(del_var)]['{}'.format(specname)]['N2CB_Tvib_value'] = stvv
                target_dict['{}'.format(bin_var)]['{}'.format(del_var)]['{}'.format(specname)]['N2CB_Tvib_stdrr'] = stvd
                target_dict['{}'.format(bin_var)]['{}'.format(del_var)]['{}'.format(specname)]['N2PlusBX_Trot_value'] = ftrv
                target_dict['{}'.format(bin_var)]['{}'.format(del_var)]['{}'.format(specname)]['N2PlusBX_Trot_stdrr'] = ftrd
                target_dict['{}'.format(bin_var)]['{}'.format(del_var)]['{}'.format(specname)]['N2PlusBX_Tvib_value'] = ftvv
                target_dict['{}'.format(bin_var)]['{}'.format(del_var)]['{}'.format(specname)]['N2PlusBX_Tvib_stdrr'] = ftvd
            self.data_file=target_dict
            GI_plotter.choices_and_checkbuttons(self)

            self.Buttons_and_stuff()
            self.loaded=True
        return self.data_file

    def save_file(self):
        """Save the current file as a new file."""
        #need to add loading from target dict
        filepath = askdirectory()
        # save_file=filepath+'\\Master_plotter_txts'
        # if not os.path.exists(save_file'\\{}delay{}bin'.format(sp1[0],s1[0])):
        #     os.makedirs(r'D:\FIles\Work_files\work\Eindhoven_work\ratios\oes_json_files\seq_delay_N2_75mbar_4kV\for_siebe\{}'.format(desic[-1],sp1[0],s1[0]))
        # np.savetxt(r'D:\FIles\Work_files\work\Eindhoven_work\ratios\oes_json_files\seq_delay_N2_75mbar_4kV\for_siebe\{}\bin{}delay{}ns.txt'.format(desic[-1],sp1[0],s1[0]),np.c_[sp_pos,strv_arr,strd_arr,stvv_arr,stvd_arr,ftrv_arr,ftrd_arr,ftvv_arr,ftvd_arr], delimiter=",", fmt='%s', header="Pixel position,N2CB_Trot_value,N2CB_Trot_stdrr,N2CB_Tvib_value,N2CB_Tvib_stdrr,N2PlusBX_Trot_value,N2PlusBX_Trot_stdrr,N2PlusBX_Tvib_value,N2PlusBX_Tvib_stdrr")
#


    def change_all_spec(self):
        if self.check_spec[0].instate(['selected'])==True:
            for i in range(len(self.check_spec)):

                self.check_spec[i].state(['!selected'])
        elif self.check_spec[0].instate(['selected'])==False:
            for i in range(len(self.check_spec)):

                self.check_spec[i].state(['selected'])

    def change_all_bins(self):
        if self.check_bins[0].instate(['selected'])==True:
            for i in range(len(self.check_bins)):

                self.check_bins[i].state(['!selected'])
        elif self.check_bins[0].instate(['selected'])==False:
            for i in range(len(self.check_bins)):

                self.check_bins[i].state(['selected'])

    def change_all_delays(self):
        if self.check_dly[0].instate(['selected'])==True:
            for i in range(len(self.check_dly)):

                self.check_dly[i].state(['!selected'])
        elif self.check_dly[0].instate(['selected'])==False:
            for i in range(len(self.check_dly)):

                self.check_dly[i].state(['selected'])

class get_vars:
    def get_delays(self):
        delays=[]
        for i in range(len(self.check_dly)):
            if self.check_dly[i].instate(['selected'])==True:
                delays.append(self.delays_choice[i])
        return delays

    def get_bins(self):
        bins=[]
        for i in range(len(self.check_bins)):
            if self.check_bins[i].instate(['selected'])==True:
                bins.append(self.bins_choice[i])
        return bins

    def get_species(self):
        species=[]
        for i in range(len(self.check_spec)):
            if self.check_spec[i].instate(['selected'])==True:
                species.append(self.species_choice[i])
        return species

    def get_y_lim(self):
        y_lim=(self.y_low.get(),self.y_high.get())
        return y_lim

    def get_std(self):
        return self.max_std.get()

    def get_fontsize(self):
        return self.font.get()


class Math_and_plot:
    def initial_plot_conditions():
        fns_head_switch=False #Display central position of FNS peak my lord?
        fns_e_switch=False #Display 1/e mark?
        sps_head_switch=False
        sps_e_switch=False
        del_points=False

        switches=array([fns_head_switch,fns_e_switch,sps_head_switch,sps_e_switch,del_points])
        return (switches)

    def initial_plot(self):
        """#nested dictionary,what you wanna fit, y limit of axis, max of std to plot"""
        switches=Math_and_plot.initial_plot_conditions()
        self.textbox.configure(state="normal")

        GI_plotter.clearTextInput(self)

        fontsize=get_vars.get_fontsize(self)
        std_limit=get_vars.get_std(self)
        y_limits=get_vars.get_y_lim(self)
        delays_array=get_vars.get_delays(self)
        bins_array=get_vars.get_bins(self)
        Temp_type=get_vars.get_species(self)
        arr_switch=False
        c_temp=len(Temp_type)
        if len(Temp_type)==1:
            arr_switch=True
        if len(Temp_type)>1:
            for i in range(len(Temp_type)):
                Temp_type[i]=str(Temp_type[i])
        else:
            Temp_type=Temp_type[0]


        target_dict=self.data_file


        if len(bins_array)==0:
            bins_array=target_dict.keys()

        if arr_switch==True:
            GI_plotter.print_in_gui(self,"Species used in plots are: "+ "".join([*map(str, Temp_type)]))
        else:
            GI_plotter.print_in_gui(self,"Species used in plots are: "+ ", ".join([*map(str, Temp_type)]))
        GI_plotter.print_in_gui(self,"Bins used in plots are: "+ ", ".join([*map(str, bins_array)]))
        plot_check=True
        del_check=False
        no_bin_array=[]
        no_dly_array=[]
        no_spec_array=[]
        title_arr=[]
        c_len=[]
        count=0

        if arr_switch==True:
            Temp_type_c=[Temp_type]
        else:
            Temp_type_c=Temp_type
        for temp_var_c in Temp_type_c:
            for bins_c in bins_array:
                for dly_c in target_dict['{}'.format(bins_c)].keys():
                    if dly_c in delays_array:
                        count+=1
                    elif dly_c not in delays_array and delays_array==[]:
                        count+=1
        c_len=count*len(bins_c)

        color=iter(cm.rainbow(linspace(0,1,int(c_len))))
        while plot_check==True:
            if arr_switch==True:
                Temp_type=[Temp_type]
            for temp_var in Temp_type:
                temp_pos1,temp_pos2=Math_and_plot.nice_title(temp_var)
                title=temp_pos1+' '+temp_pos2+' temperature'
                if arr_switch==False:
                    title_arr.append(title)
                spt_dic = defaultdict(dict)
                temp_dic = defaultdict(dict)
                for bins in bins_array:
                    if len(delays_array)==0:
                        GI_plotter.print_in_gui(self,"Delays used for {}bin in {} plot are: ".format(bins,temp_var)+ ", ".join([*map(str, target_dict['{}'.format(bins)].keys())])+" ns")
                        for dly in target_dict['{}'.format(bins)].keys():
                            try:
                                temp=Math_and_plot.get_val(target_dict,bins,dly,temp_var+'_value')
                            except KeyError:
                                GI_plotter.print_in_gui(self,'Combination of bin {} and delay {}ns doesnt exist.'.format(bins, dly))
                                continue
                            c=next(color)
                            temp=Math_and_plot.get_val(target_dict,bins,dly,temp_var+'_value')
                            std=Math_and_plot.get_val(target_dict,bins,dly,temp_var+'_stdrr')
                            spt=list(map(int, target_dict["{}".format(bins)]['{}'.format(dly)]))
                            del_idx=[]
                            for i in range(len(std)):
                                if std[i]>std_limit:
                                    del_idx.append(i)
                            std_del=delete(std, del_idx).tolist()
                            temp_del=delete(temp, del_idx).tolist()
                            spt_del=delete(spt, del_idx).tolist()

        #                     spt_dic[bins][dly]={}
                            spt_dic['{}'.format(bins)]['{}'.format(dly)]=spt_del
        #                     temp_dic[bins][dly]={}
                            temp_dic['{}'.format(bins)]['{}'.format(dly)]=temp_del

                            if str(bins) in no_bin_array:
                                if str(dly) in no_dly_array:
                                    # print(bins,dly)
                                    std_del=delete(std_del, no_spec_array).tolist()
                                    temp_del=delete(temp_del, no_spec_array).tolist()
                                    spt_del=delete(spt_del, no_spec_array).tolist()

                            plt.errorbar(spt_del,temp_del,std_del, elinewidth=2, capsize=4,label='{}: {}ns delay {}bin'.format(temp_var,dly,bins),c=c)
                            plt.ylim(y_limits)

                            plt.legend(fontsize=fontsize-10)
                            plt.xticks(fontsize=fontsize-2)
                            plt.yticks(fontsize=fontsize-2)
                #                 plt.xlabel('Spatial axis binned by 4',fontsize=fontsize)
                            plt.xlabel('Spatial axis',fontsize=fontsize)

                            plt.ylabel('Temperature [K]',fontsize=fontsize)
                            plt.grid(True)

                            # if int(dly)<dly_lim:
                            #     if switches[0]==True:
                            #         plt.axvline(head_dict['FNS']['{}'.format(dly)]['central_head'],c=c)
                            #     if switches[1]==True:
                            #         plt.axvline(head_dict['FNS']['{}'.format(dly)]['e_head'],linestyle='--',c=c)
                            #     if switches[2]==True:
                            #         plt.axvline(head_dict['SPS']['{}'.format(dly)]['central_head'],c=c)
                            #     if switches[3]==True:
                            #         plt.axvline(head_dict['SPS']['{}'.format(dly)]['e_head'],linestyle='--',c=c)



        #                 plt.show(block=True)
                    else:
                        # color=iter(cm.rainbow(np.linspace(0,1,int(len(target_dict['{}'.format(bins)].keys())))))
                        GI_plotter.print_in_gui(self,"Delays used for {}bin in {} plot are: ".format(bins,temp_var)+ ", ".join([*map(str, delays_array)])+" ns")
                        for dly in delays_array:

                            try:
                                temp=Math_and_plot.get_val(target_dict,bins,dly,temp_var+'_value')
                            except KeyError:
                                GI_plotter.print_in_gui(self,'Combination of bin {} and delay {}ns doesnt exist.'.format(bins, dly))
                                continue
                            c=next(color)
                            temp=Math_and_plot.get_val(target_dict,bins,dly,temp_var+'_value')
                            std=Math_and_plot.get_val(target_dict,bins,dly,temp_var+'_stdrr')
                            spt=list(map(int, target_dict["{}".format(bins)]['{}'.format(dly)]))
                            del_idx=[]
                            for i in range(len(std)):
                                if std[i]>std_limit:
                                    del_idx.append(i)
                            std_del=delete(std, del_idx).tolist()
                            temp_del=delete(temp, del_idx).tolist()
                            spt_del=delete(spt, del_idx).tolist()

        #                     spt_dic[bins][dly]={}
                            spt_dic['{}'.format(bins)]['{}'.format(dly)]=spt_del
        #                     temp_dic[bins][dly]={}
                            temp_dic['{}'.format(bins)]['{}'.format(dly)]=temp_del

                            if str(bins) in no_bin_array:
                                if str(dly) in no_dly_array:
                                    # print(bins,dly)
                                    std_del=delete(std_del, no_spec_array).tolist()
                                    temp_del=delete(temp_del, no_spec_array).tolist()
                                    spt_del=delete(spt_del, no_spec_array).tolist()

                            plt.errorbar(spt_del,temp_del,std_del, elinewidth=2, capsize=4,label='{}: {}ns delay {}bin'.format(temp_var,dly,bins),c=c)
                            plt.ylim(y_limits)


                            plt.legend(fontsize=fontsize-10)
                            plt.xticks(fontsize=fontsize-2)
                            plt.yticks(fontsize=fontsize-2)
                #                 plt.xlabel('Spatial axis binned by 4',fontsize=fontsize)
                            plt.xlabel('Spatial axis',fontsize=fontsize)

                            plt.ylabel('Temperature [K]',fontsize=fontsize)
                            plt.grid(True)
                            # if int(dly)<dly_lim:
                            #     if switches[0]==True:
                            #         plt.axvline(head_dict['FNS']['{}'.format(dly)]['central_head'],c=c)
                            #     if switches[1]==True:
                            #         plt.axvline(head_dict['FNS']['{}'.format(dly)]['e_head'],linestyle='--',c=c)
                            #     if switches[2]==True:
                            #         plt.axvline(head_dict['SPS']['{}'.format(dly)]['central_head'],c=c)
                            #     if switches[3]==True:
                            #         plt.axvline(head_dict['SPS']['{}'.format(dly)]['e_head'],linestyle='--',c=c)
            if arr_switch==False:
                plt.title(", ".join([*map(str, title_arr)]),fontsize=fontsize-2)
            else:
                plt.title(title,fontsize=fontsize-2)
            plt.show(block=False)

            if switches[4]==True and del_check==False:
                loc=plt.ginput(1)
                if loc[0][0]<300 and loc[0][1]<300:
                    break


                no_bin,no_dly,no_spec=find_nearest_in_dic(spt_dic,temp_dic,loc)

                GI_plotter.print_in_gui(self,"Locations of points to delete: {}, {}".format(loc[0][0],loc[0][1]))
                GI_plotter.print_in_gui(self,"found position keys: {},{},{}".format(no_bin,no_dly,no_spec))
                GI_plotter.print_in_gui(self,"found position: {}".format(spt_dic['{}'.format(no_bin)]['{}'.format(no_dly)][no_spec]))
                no_bin_array.append(no_bin)
                no_dly_array.append(no_dly)
                no_spec_array.append(no_spec)
                plot_check=True
                del_check=False
                plt.close()

            else:
                plot_check=False
            self.textbox.configure(state="disabled")




    def mark_head(head_dict,dly,switches):
        """ Just a switcher function for head display"""
        if switches[0]==True:
            plt.axvline(head_dict['FNS']['{}'.format(dly)]['central_head'])
        if switches[1]==True:
            plt.axvline(head_dict['FNS']['{}'.format(dly)]['e_head'],linestyle='--')
        if switches[2]==True:
            plt.axvline(head_dict['SPS']['{}'.format(dly)]['central_head'])
        if switches[3]==True:
            plt.axvline(head_dict['SPS']['{}'.format(dly)]['e_head'],linestyle='--')

    def find_nearest_in_dic(dic_x,dic_y,value):
        """
        Find closest match of value in a dictionary, uses minimization of a square where the next point has to be smaller then the previouse
        """
        prev_diff=1e6
        value_x=value[0][0]
        value_y=value[0][1]
        for bin_key in dic_x.keys():
    #         print(dic.keys(),dic['{}'.format(bin_key)].keys())
            for dly_key in dic_x['{}'.format(bin_key)].keys():
                diff = abs(dic_x[bin_key][dly_key]-value_x)+abs(dic_y[bin_key][dly_key]-value_y)
    #             print(dic[bin_key][dly_key],value,bin_key,dly_key)
                for spec_pos in range(len(diff)):
                    if diff[spec_pos]<prev_diff:
                        # print(prev_diff,diff[spec_pos],bin_key,dly_key)
                        prev_diff=diff[spec_pos]
                        res_bin=bin_key
                        res_dly=dly_key
                        spec_idx=spec_pos
    #     print(res_bin,res_dly,spec_idx)
        return res_bin,res_dly,spec_idx

    def find_nearest(array,value):
        """
        Find closest match of value in an array
        """
        idx = (abs(array-value)).argmin()
        return idx

    def get_val(dic,bins,delay,what): #create better variation to seperate value and stddtr
        """Function to get All the values of type "what" witch specific number of "bins" and at specific "delay" from a specific "nested dictionary"  """
        values=[]
    #     print(dic['{}'.format(bins)],bins)
        for spec in dic['{}'.format(bins)]['{}'.format(delay)].keys():
            temp=dic['{}'.format(bins)]['{}'.format(delay)][spec][what]
            if temp==None: #if the fit result puts here None as a result, input
                temp=9e6 #some high value so we can plot it (large deviations are taken care of in function plotting_fun)
            values.append(temp)
        values=array(values)
        return values

    def nice_title(Temp_type):
        """Function to get nice plots based on temperature Temp_type string"""
        # print(Temp_type)
        if Temp_type=='N2CB_Tvib':
            temp_pos1='N$_2$(C-B)'
            temp_pos2='vibrational'
        elif Temp_type=='N2CB_Trot':
            temp_pos1='N$_2$(C-B)'
            temp_pos2='rotational'
        elif Temp_type=='N2PlusBX_Tvib':
            temp_pos1='N$_2^+$(B-X)'
            temp_pos2='vibrational'
        elif Temp_type=='N2PlusBX_Trot':
            temp_pos1='N$_2^+$(B-X)'
            temp_pos2='rotational'
        return temp_pos1, temp_pos2



root = tk.Tk()
gui=GI_plotter(root)
root.mainloop()
