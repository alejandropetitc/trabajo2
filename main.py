class Vnt:
    est_validos = ["O", "XO", "OXO", "OXXO"]
    acb_validos = ["Pulido", "Lacado Brillante", "Lacado Mate", "Anodizado"]
    vid_validos = ["Transparente", "Bronce", "Azul"]

    def __init__(self, est, an, al, acb_alu, tipo_vid, esm, tipo_x=False):
        self.est = self.val_est(est)
        self.an = self.val_dim(an, "ancho")
        self.al = self.val_dim(al, "alto")
        self.acb_alu = self.val_acb(acb_alu)
        self.tipo_vid = self.val_vid(tipo_vid)
        self.esm = self.val_bool(esm, "esmerilado")
        self.tipo_x = self.val_bool(tipo_x, "tipo X")
        self.esc = 4  # Esquinas por ventana
        self.desc_vol = 0.10  # Descuento por volumen
        self.cst_tot = 0
        self.perfiles_nave = self.calc_perf_nave()

    def val_est(self, est):
        if est not in self.est_validos:
            raise ValueError(f"Estilo '{est}' no es válido. Debe ser uno de: {self.est_validos}")
        return est

    def val_dim(self, val, nom):
        if val <= 0:
            raise ValueError(f"El valor del {nom} debe ser mayor que cero. Valor ingresado: {val}")
        return val

    def val_acb(self, acb_alu):
        if acb_alu not in self.acb_validos:
            raise ValueError(f"Acabado de aluminio '{acb_alu}' no es válido. Debe ser uno de: {self.acb_validos}")
        return acb_alu

    def val_vid(self, tipo_vid):
        if tipo_vid not in self.vid_validos:
            raise ValueError(f"Tipo de vidrio '{tipo_vid}' no es válido. Debe ser uno de: {self.vid_validos}")
        return tipo_vid

    def val_bool(self, val, nom):
        if not isinstance(val, bool):
            raise ValueError(f"El campo '{nom}' debe ser True o False. Valor ingresado: {val}")
        return val

    def calc_perf_nave(self):
        if self.est == "O":
            return 1
        elif self.est == "XO":
            return 2
        elif self.est == "OXO":
            return 3
        elif self.est == "OXXO":
            return 4
        else:
            raise ValueError("Estilo de ventana no válido")

    def calc_cst_alu(self):
        # Costo del aluminio por metro lineal
        cst_metro = 50
        peri_nave = 2 * (self.an + self.al)
        total_perf = peri_nave * self.perfiles_nave
        return total_perf * cst_metro

    def calc_cst_vid(self):
        # Costo del vidrio por cm²
        cst_vid_base = 0.2
        an_vid = self.an - 1.5 * 2
        al_vid = self.al - 1.5 * 2
        area_vid = an_vid * al_vid
        cst_vid = area_vid * cst_vid_base

        # Si es esmerilado, añadir 10% al costo
        if self.esm:
            cst_vid += cst_vid * 0.10

        return cst_vid

    def calc_cst_esc(self):
        # Costo por esquina
        cst_esc = 5
        return self.esc * cst_esc

    def calc_cst_ch(self):
        # Costo de la chapa si es tipo X
        if self.tipo_x:
            return 20
        return 0

    def calc_cst_tot(self, cant):
        # Suma todos los costos de la ventana
        cst_alu = self.calc_cst_alu()
        cst_vid = self.calc_cst_vid()
        cst_esc = self.calc_cst_esc()
        cst_ch = self.calc_cst_ch()

        # Total sin descuento
        self.cst_tot = cst_alu + cst_vid + cst_esc + cst_ch

        # Aplicar descuento si hay más de 100 ventanas
        if cant > 100:
            self.cst_tot -= self.cst_tot * self.desc_vol

        return self.cst_tot


def gen_cot(vnts):
    total_gen = 0
    print("\n--- Cotización de Ventanas ---")
    for i, vnt in enumerate(vnts):
        try:
            cst = vnt.calc_cst_tot(len(vnts))
            total_gen += cst
            print(f"Ventana {i + 1}:")
            print(f"  Estilo: {vnt.est}")
            print(f"  Dimensiones: {vnt.an} x {vnt.al} cm")
            print(f"  Acabado Aluminio: {vnt.acb_alu}")
            print(f"  Tipo de Vidrio: {vnt.tipo_vid} {'Esmerilado' if vnt.esm else ''}")
            print(f"  Costo Total: ${cst:.2f}\n")
        except ValueError as e:
            print(f"Error en ventana {i + 1}: {e}")
    
    print(f"Total General: ${total_gen:.2f}")
    return total_gen


# Ejemplo de uso
try:
    vnt1 = Vnt(est="XO", an=120, al=150, acb_alu="Lacado Brillante", tipo_vid="Transparente", esm=False)
    vnt2 = Vnt(est="OXXO", an=180, al=120, acb_alu="Pulido", tipo_vid="Bronce", esm=True, tipo_x=True)
    vnts = [vnt1, vnt2]

    # Generar cotización
    gen_cot(vnts)

except ValueError as e:
    print(f"Error al crear la ventana: {e}")
