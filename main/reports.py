from . import excel
import uuid
from main.serializers.company import BusinessCompanyRegSerializer
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)
from main.serializers.psmt import (
    PIDVARequestDetailSerializer,
    PSMTRequestDetailSerializer,
    PSMTRequestSerializer,
    RequestSerializer,
)
from .models import PSMTRequest , PelPsmtRequestModules
from . import custom_query



def ngo_report (client_login_id,data,mcode):
    cname='temp/ngo_'+str(uuid.uuid4())+'.xlsx'
    workbook=excel.generateWorkbook(cname)
    worksheet=excel.getWorksheet(workbook)
    bold = workbook.add_format({'bold': True})
    excel.addHeader(worksheet,0,"Client No")
    excel.addHeader(worksheet,1,"Company Name")       
    excel.addHeader(worksheet,2,"Reg no") 
    excel.addHeader(worksheet,3,"Country")
    row=1
    for rdata in data:
        row+= 1
        excel.addData(worksheet,row,0,rdata[0])
        excel.addData(worksheet,row,1,rdata[1])
        excel.addData(worksheet,row,2,rdata[2])
        excel.addData(worksheet,row,3,rdata[3]) 
        b_data=custom_query.ngo_society_sacco_trust_official_details(rdata[2])
        #check if mcode is TR theb it will be trustees else officials
        row+= 1
         
        if mcode == 'TR' :
          excel.addHeaderAtRow(worksheet,row,3,'Trustees',bold)
        else:
          excel.addHeaderAtRow(worksheet,row,3,'Officials',bold)         
        for rbdata in b_data:
            row+= 1
            excel.addData(worksheet,row,3,rbdata[19])
            excel.addData(worksheet,row,4,rbdata[20])
            row+= 1
        row+= 1    
    workbook.close()
    return cname

def company_report (client_login_id,data,mcode):
    cname='temp/co_'+str(uuid.uuid4())+'.xlsx'
    workbook=excel.generateWorkbook(cname)
    bold = workbook.add_format({'bold': True})
    worksheet=excel.getWorksheet(workbook)
    row=0
    first_row=1
    for rdata in data:
            #print(rdata)   
            excel.addHeaderAtRow(worksheet,row,0,'Client No',bold) 
            excel.addHeaderAtRow(worksheet,row,1,'Company Name',bold) 
            excel.addHeaderAtRow(worksheet,row,2,'Registration no',bold) 
            excel.addHeaderAtRow(worksheet,row,3,'Physical Address',bold) 
            excel.addHeaderAtRow(worksheet,row,4,'Postal Address',bold)
            excel.addHeaderAtRow(worksheet,row,5,'Registered Telephone',bold)
            excel.addHeaderAtRow(worksheet,row,6,'Registered Email',bold)
            excel.addHeaderAtRow(worksheet,row,7,'Country',bold)
            row+=1
            excel.addData(worksheet,row,0,rdata[9])
            excel.addData(worksheet,row,1,rdata[1])
            excel.addData(worksheet,row,2,rdata[8])
            #excel.addData(worksheet,row,3,rdata[9])     
            #excel.addData(worksheet,row,4,rdata[16])  
            #excel.addData(worksheet,row,5,rdata[6])  
            #excel.addData(worksheet,row,6,rdata[5])
            #excel.addData(worksheet,row,7,rdata[4])     
            #print(row )
            row+=1
            if mcode == 'CO' or mcode == 'ICO':
             excel.addHeaderAtRow(worksheet,row,1,'Shareholders',bold)
            if mcode == 'CLG' or mcode == 'BN':
             excel.addHeaderAtRow(worksheet,row,1,'Owners',bold)             
            row+=1 
            excel.addHeaderAtRow(worksheet,row,1,'First Name',bold) 
            excel.addHeaderAtRow(worksheet,row,2,'Second Name',bold) 
            excel.addHeaderAtRow(worksheet,row,3,'Shares Number',bold) 
            #excel.addHeaderAtRow(worksheet,row,4,'Nominal Value',bold) 
            excel.addHeaderAtRow(worksheet,row,4,'Citizenship',bold) 
            excel.addHeaderAtRow(worksheet,row,5,'Address',bold) 
            excel.addHeaderAtRow(worksheet,row,6,'Description',bold) 
            row+=1
            b_data=custom_query.company_bussiness_clg(rdata[2])
            for rbdata in b_data:
                excel.addData(worksheet,row,1,rbdata[31])
                excel.addData(worksheet,row,2,rbdata[32])
                excel.addData(worksheet,row,3,rbdata[46])
               # excel.addData(worksheet,row,4,rbdata[56])
                excel.addData(worksheet,row,4,rbdata[56])
                excel.addData(worksheet,row,5,rbdata[35])
                excel.addData(worksheet,row,6,rbdata[55])

                # now we have company data

                excel.addData(worksheet,first_row,3,rbdata[8])
                excel.addData(worksheet,first_row,4,rbdata[15])
                excel.addData(worksheet,first_row,5,rbdata[3])
                excel.addData(worksheet,first_row,6,rbdata[1])
                excel.addData(worksheet,first_row,7,rbdata[5])
                row+=1

            if mcode == 'CO' or mcode == 'ICO':
                    excel.addHeaderAtRow(worksheet,row,1,'Share Capital',bold)
                    row+=1
                    excel.addHeaderAtRow(worksheet,row,1,'Name',bold)
                    excel.addHeaderAtRow(worksheet,row,2,'Nominal Value',bold) 
                    excel.addHeaderAtRow(worksheet,row,3,'No of Shares',bold)
                    row+= 1
                    nominal_data= custom_query.nominal_shares(rdata[2])
                    for ndata in nominal_data:           
                        excel.addData(worksheet,row,1,ndata[5])
                        excel.addData(worksheet,row,2,ndata[4])
                        excel.addData(worksheet,row,3,ndata[3])
                        row+= 1


                    excel.addHeaderAtRow(worksheet,row,1,'Encumberances',bold) 
                    row+= 1
                    excel.addHeaderAtRow(worksheet,row,2,'DESCRIPTION',bold) 
                    excel.addHeaderAtRow(worksheet,row,3,'DATE OF INSTRUMENT',bold) 
                    excel.addHeaderAtRow(worksheet,row,4,'AMOUNT SECURED',bold)     
                    encumerence_data=custom_query.encumburances(rdata[2]) 
                    row+= 1
                    #print(encumerence_data)
                    for ebdata in encumerence_data:
                            excel.addData(worksheet,row,2,ebdata[3])
                            excel.addData(worksheet,row,3,ebdata[4])
                            excel.addData(worksheet,row,4,ebdata[5])
                            row+=1               
            row+=1
            first_row=row+1        
    workbook.close()
    return cname  

def unknown_report (client_login_id,data,mcode):
    cname='temp/unk_'+str(uuid.uuid4())+'.xlsx'
    workbook=excel.generateWorkbook(cname)
    bold = workbook.add_format({'bold': True})
    worksheet=excel.getWorksheet(workbook)
    row=0
    for rdata in data:
        #print(rdata)
        excel.addHeaderAtRow(worksheet,row,0,'Client No',bold) 
        excel.addHeaderAtRow(worksheet,row,1,'Company Name',bold) 
        excel.addHeaderAtRow(worksheet,row,2,'Registration no',bold) 
        excel.addHeaderAtRow(worksheet,row,3,'Request Ref',bold) 
        row+=1
        excel.addData(worksheet,row,0,rdata[9])
        excel.addData(worksheet,row,1,rdata[1])
        excel.addData(worksheet,row,2,rdata[8])
        excel.addData(worksheet,row,3,rdata[0])

    workbook.close()
    return cname      

