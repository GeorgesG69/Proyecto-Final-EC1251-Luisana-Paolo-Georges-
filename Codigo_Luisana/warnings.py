  # -Warnings- #
Escritor_Warnings = pd.ExcelWriter("data_io.xlsx", mode="a", if_sheet_exists="overlay")

# -V fuente
for i in range(len(Nodo_V_fuente_i)):

    if (V_pico_V_fuente[i] < 0):
        IndiceVPNeg = [valor for valor, dato in enumerate(V_pico_V_fuente) if dato < 0]
        DfWarnings_V.loc[IndiceVPNeg, "Warning"] = "Valor pico no puede ser negativo"

        DfWarnings_V.to_excel(Escritor_Warnings, "V_fuente", index=False)
        Escritor_Warnings.close() 

        raise TypeError("Valor pico no puede ser negativo")

    if (Res_V_fuente[i] < 0) or (Ind_V_fuente[i] < 0) or (Cap_V_fuente[i] < 0):

        IndiceVPNeg = [valor for valor, dato in enumerate(Res_V_fuente) if dato < 0]
        DfWarnings_V.loc[IndiceVPNeg, "Warning"] = "Res/Ind/Cap no puede ser negativo."   

        IndiceVPNeg = [valor for valor, dato in enumerate(Ind_V_fuente) if dato < 0]
        DfWarnings_V.loc[IndiceVPNeg, "Warning"] = "Res/Ind/Cap no puede ser negativo." 

        IndiceVPNeg = [valor for valor, dato in enumerate(Cap_V_fuente) if dato < 0]
        DfWarnings_V.loc[IndiceVPNeg, "Warning"] = "Res/Ind/Cap no puede ser negativo." 

        DfWarnings_V.to_excel(Escritor_Warnings, "V_fuente", index=False)
        Escritor_Warnings.close() 

        raise TypeError("(V) Res/Ind/Cap no puede ser negativo.")

# -I fuente
for i in range(len(Nodo_I_fuente_i)):

    if (I_pico_I_fuente[i] < 0):
        IndiceVPNeg = [valor for valor, dato in enumerate(I_pico_I_fuente) if dato < 0]
        DfWarnings_I.loc[IndiceVPNeg, "Warning"] = "Valor pico no puede ser negativo"

        DfWarnings_I.to_excel(Escritor_Warnings, "I_fuente", index=False)
        Escritor_Warnings.close() 

        raise TypeError("Valor pico no puede ser negativo")

    if (Res_I_fuente[i] < 0) or (Ind_I_fuente[i] < 0) or (Cap_I_fuente[i] < 0):
        IndiceVPNeg = [valor for valor, dato in enumerate(Res_I_fuente) if dato < 0]
        DfWarnings_I.loc[IndiceVPNeg, "Warning"] = "Res/Ind/Cap no puede ser negativo."   

        IndiceVPNeg = [valor for valor, dato in enumerate(Ind_I_fuente) if dato < 0]
        DfWarnings_I.loc[IndiceVPNeg, "Warning"] = "Res/Ind/Cap no puede ser negativo." 

        IndiceVPNeg = [valor for valor, dato in enumerate(Cap_I_fuente) if dato < 0]
        DfWarnings_I.loc[IndiceVPNeg, "Warning"] = "Res/Ind/Cap no puede ser negativo." 

        DfWarnings_I.to_excel(Escritor_Warnings, "I_fuente", index=False)
        Escritor_Warnings.close() 

        raise TypeError("Res/Ind/Cap no puede ser negativo.")
    
# -Z
for i in range(len(Nodo_Z_i)):

    if (Res_Z[i] < 0) or (Ind_Z[i] < 0) or (Cap_Z[i] < 0):
       
       IndiceVPNeg = [valor for valor, dato in enumerate(Res_Z) if dato < 0]
       DfWarnings_Z.loc[IndiceVPNeg, "Warning"] = "Res/Ind/Cap no puede ser negativo."
        
       IndiceVPNeg = [valor for valor, dato in enumerate(Ind_Z) if dato < 0]
       DfWarnings_Z.loc[IndiceVPNeg, "Warning"] = "Res/Ind/Cap no puede ser negativo." 

       IndiceVPNeg = [valor for valor, dato in enumerate(Cap_Z) if dato < 0]
       DfWarnings_Z.loc[IndiceVPNeg, "Warning"] = "Res/Ind/Cap no puede ser negativo." 

       DfWarnings_Z.to_excel(Escritor_Warnings, "Z", index=False)
       Escritor_Warnings.close()     

       raise TypeError("(Z) Res/Ind/Cap no puede ser negativo.")
