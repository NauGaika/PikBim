# coding: utf8
"""Добавляем необходимые фильтры для КЖ"""
from math import pi
from Autodesk.Revit.DB import Transaction, ElementId

from Autodesk.Revit.DB.Structure import RebarInSystem, Rebar
from System.Collections.Generic import List



uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
curview = uidoc.ActiveGraphicalView
selection = [doc.GetElement(elId) for elId in __revit__.ActiveUIDocument.Selection.GetElementIds()]

rebar_resistance = {
    400: 355,
    500: 435 
}

concrete_resistance = {
    15: 7.5,
    20: 0.9,
    25: 1.05,
    30: 1.15,
    35: 1.3,
    40: 1.4,
    45: 1.5
}

def get_perep(ancer_base, diam, koef):
    if round(ancer_base * koef / diam) < ancer_base * koef / diam:
        return round(ancer_base * koef / diam + 1)
    else:
        return round(ancer_base / diam * koef)

if selection:
    if isinstance(selection[0], Rebar):
        el = selection[0]
        el_type = doc.GetElement(el.GetTypeId())
        diam = int(to_mm(el_type.GetParameters('Рзм.Диаметр')[0].AsDouble()))
        concrete = int(el_type.GetParameters('Арм.КлассБетона')[0].AsDouble())
        rebar_class = int(el_type.GetParameters('Арм.КлассЧисло')[0].AsDouble())
        cur_con_res = concrete_resistance[concrete]
        cur_reb_res = rebar_resistance[rebar_class]

        ancer_base = (cur_reb_res * diam**2 * pi/4)/(cur_con_res * 2.5 * diam * pi)
        compress_anc = get_perep(ancer_base, diam, 0.75)*  diam
        bend_anc = get_perep(ancer_base, diam, 1)*  diam
        perep_bend = get_perep(ancer_base, diam, 1.2)*  diam
        perep_compr = get_perep(ancer_base, diam, 0.9)*  diam
        perep_sesm =  perep_bend * 1.3

        perep_comp_100 = get_perep(ancer_base, diam, 1.4)*  diam
        perep_comp_100_sesm = round(get_perep(ancer_base, diam, 1.4) * 1.3) *  diam
        perep_bend_100 = get_perep(ancer_base, diam, 2)*  diam
        perep_bend_100_sesm = round(get_perep(ancer_base, diam, 2) * 1.3) *  diam

        message(
            """
            Длина анкеровки(сжатых стержней), {} мм
            Длина анкеровки(растянутых стержней), {} мм
            Длина перпуска(растянутые стержни), {} мм
            Длина перпуска(сжатые стержни), {} мм
            Длина перпуска(сейсмика), {} мм
            Длина перепуска 100% одно сеч. с отгибами (раст.), {} мм
            Длина перепуска 100% одно сеч. с прямыми (раст.), {} мм
            Длина перепуска 100% одно сеч. с отгибами (раст.) сейсм, {} мм
            Длина перепуска 100% одно сеч. с прямыми (раст.) сейсм, {} мм

            """.format(
            compress_anc,
            bend_anc,
            perep_bend,
            perep_compr,
            perep_sesm,
            perep_comp_100,
            perep_comp_100_sesm,
            perep_bend_100,
            perep_bend_100_sesm))


# t=Transaction(doc, 'tt')
# t.Start()
# if selection:
#     if isinstance(selection[0], RebarInSystem):
#         __revit__.ActiveUIDocument.Selection.SetElementIds(List[ElementId]([selection[0].SystemId]))
# t.Commit()