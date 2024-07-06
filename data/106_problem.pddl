
(define (problem electroplating)
        (:domain Electroplating)
        (:objects

                pole1 - pole
                pole2 - pole
                pole3 - pole
                pole4 - pole
                pole5 - pole
                pole6 - pole
                pole7 - pole
                pole8 - pole
                pole9 - pole
                pole10 - pole
                pole11 - pole
                gear1 - pole
                gear2 - pole
                slot1 - slot
                slot2 - slot
                slot3 - slot
                slot4 - slot
                slot5 - slot
                slot6 - slot
                slot7 - slot
                slot8 - slot
                slot9 - slot
                slot10 - slot
                slot11 - slot
                slot12 - slot
                slot13 - slot
                slot14 - slot
                slot15 - slot
                slot16 - slot
                slot17 - slot
                slot18 - slot
                slot19 - slot
                slot20 - slot
                slot21 - slot
                slot22 - slot
                slot23 - slot
                slot24 - slot
                slot25 - slot
                slot26 - slot
                slot27 - slot
                slot28 - slot
                slot29 - slot
                slot30 - slot
                slot31 - slot
                slot32 - slot
                slot33 - slot
                slot34 - slot
                slot35 - slot
                slot36 - slot
                slot37 - slot
                slot38 - slot
                slot39 - slot
                slot40 - slot
                slot41 - slot
                slot42 - slot
                slot43 - slot
                slot44 - slot
                slot45 - slot
                slot46 - slot
                slot47 - slot
                slot48 - slot
                slot49 - slot
                slot60 - slot
                slot61 - slot
                slot62 - slot
                slot63 - slot
                slot64 - slot
                slot65 - slot
                slot66 - slot
                slot67 - slot
                slot68 - slot
                slot69 - slot
                slot70 - slot
                slot71 - slot
                slot72 - slot
                slot73 - slot
                slot74 - slot
                slot75 - slot
                slot76 - slot
                slot77 - slot
                slot78 - slot
                slot79 - slot
                slot80 - slot
                slot81 - slot
                slot82 - slot
                slot83 - slot
                slot84 - slot
                slot85 - slot
                slot86 - slot
                slot87 - slot
                slot88 - slot
                slot89 - slot
                slot90 - slot
                slot91 - slot
                slot92 - slot
                slot93 - slot
                slot94 - slot
                slot95 - slot
                slot96 - slot
                slot97 - slot
                slot98 - slot
                slot99 - slot
                slot100 - slot
                slot101 - slot
                slot102 - slot
                slot103 - slot
                slot104 - slot
                slot105 - slot
                slot106 - slot
                p10000 - product
        )
        (:init
                (border_slot slot1)
                (border_slot slot49)
                (border_slot slot60)
                (border_slot slot106)
                (stocking_slot slot8)
                (stocking_slot slot9)
                (stocking_slot slot10)
                (stocking_slot slot11)
                (stocking_slot slot12)
                (stocking_slot slot13)
                (blanking_slot slot2)
                (blanking_slot slot3)
                (pole_position pole1 slot7)
                (pole_stop_moving pole1)
                (slot_have_pole slot7)
                (pole_available pole1)
                (pole_empty pole1)
                (pole_region pole1 slot1)
                (pole_region pole1 slot2)
                (pole_region pole1 slot3)
                (pole_region pole1 slot4)
                (pole_region pole1 slot5)
                (pole_region pole1 slot6)
                (pole_region pole1 slot7)
                (pole_region pole1 slot8)
                (pole_region pole1 slot9)
                (pole_region pole1 slot10)
                (pole_region pole1 slot11)
                (pole_region pole1 slot12)
                (pole_region pole1 slot13)
                (pole_region pole1 slot14)
                (pole_region pole1 slot15)
                (pole_region pole1 slot16)
                (pole_region pole1 slot17)
                (pole_region pole1 slot18)
                (pole_region pole1 slot19)
                (pole_region pole1 slot20)
                (pole_position pole2 slot16)
                (pole_stop_moving pole2)
                (slot_have_pole slot16)
                (pole_available pole2)
                (pole_empty pole2)
                (pole_region pole2 slot16)
                (pole_region pole2 slot17)
                (pole_region pole2 slot18)
                (pole_region pole2 slot19)
                (pole_region pole2 slot20)
                (pole_region pole2 slot21)
                (pole_region pole2 slot22)
                (pole_region pole2 slot23)
                (pole_region pole2 slot24)
                (pole_region pole2 slot25)
                (pole_region pole2 slot26)
                (pole_region pole2 slot27)
                (pole_region pole2 slot28)
                (pole_position pole3 slot30)
                (pole_stop_moving pole3)
                (slot_have_pole slot30)
                (pole_available pole3)
                (pole_empty pole3)
                (pole_region pole3 slot27)
                (pole_region pole3 slot28)
                (pole_region pole3 slot29)
                (pole_region pole3 slot30)
                (pole_region pole3 slot31)
                (pole_region pole3 slot32)
                (pole_region pole3 slot33)
                (pole_region pole3 slot34)
                (pole_region pole3 slot35)
                (pole_region pole3 slot36)
                (pole_region pole3 slot37)
                (pole_position pole4 slot37)
                (pole_stop_moving pole4)
                (slot_have_pole slot37)
                (pole_available pole4)
                (pole_empty pole4)
                (pole_region pole4 slot35)
                (pole_region pole4 slot36)
                (pole_region pole4 slot37)
                (pole_region pole4 slot38)
                (pole_region pole4 slot39)
                (pole_region pole4 slot40)
                (pole_region pole4 slot41)
                (pole_region pole4 slot42)
                (pole_region pole4 slot43)
                (pole_region pole4 slot44)
                (pole_position pole5 slot44)
                (pole_stop_moving pole5)
                (slot_have_pole slot44)
                (pole_available pole5)
                (pole_empty pole5)
                (pole_region pole5 slot42)
                (pole_region pole5 slot43)
                (pole_region pole5 slot44)
                (pole_region pole5 slot45)
                (pole_region pole5 slot46)
                (pole_region pole5 slot47)
                (pole_region pole5 slot48)
                (pole_region pole5 slot49)
                (pole_position pole6 slot62)
                (pole_stop_moving pole6)
                (slot_have_pole slot62)
                (pole_available pole6)
                (pole_empty pole6)
                (pole_region pole6 slot60)
                (pole_region pole6 slot61)
                (pole_region pole6 slot62)
                (pole_region pole6 slot63)
                (pole_region pole6 slot64)
                (pole_region pole6 slot65)
                (pole_region pole6 slot66)
                (pole_region pole6 slot67)
                (pole_position pole7 slot66)
                (pole_stop_moving pole7)
                (slot_have_pole slot66)
                (pole_available pole7)
                (pole_empty pole7)
                (pole_region pole7 slot65)
                (pole_region pole7 slot66)
                (pole_region pole7 slot67)
                (pole_region pole7 slot68)
                (pole_region pole7 slot69)
                (pole_region pole7 slot70)
                (pole_region pole7 slot71)
                (pole_region pole7 slot72)
                (pole_region pole7 slot73)
                (pole_region pole7 slot74)
                (pole_region pole7 slot75)
                (pole_region pole7 slot76)
                (pole_region pole7 slot77)
                (pole_region pole7 slot78)
                (pole_region pole7 slot79)
                (pole_position pole8 slot72)
                (pole_stop_moving pole8)
                (slot_have_pole slot72)
                (pole_available pole8)
                (pole_empty pole8)
                (pole_region pole8 slot70)
                (pole_region pole8 slot71)
                (pole_region pole8 slot72)
                (pole_region pole8 slot73)
                (pole_region pole8 slot74)
                (pole_region pole8 slot75)
                (pole_region pole8 slot76)
                (pole_region pole8 slot77)
                (pole_region pole8 slot78)
                (pole_region pole8 slot79)
                (pole_region pole8 slot80)
                (pole_region pole8 slot81)
                (pole_region pole8 slot82)
                (pole_region pole8 slot83)
                (pole_region pole8 slot84)
                (pole_region pole8 slot85)
                (pole_region pole8 slot86)
                (pole_position pole9 slot88)
                (pole_stop_moving pole9)
                (slot_have_pole slot88)
                (pole_available pole9)
                (pole_empty pole9)
                (pole_region pole9 slot86)
                (pole_region pole9 slot87)
                (pole_region pole9 slot88)
                (pole_region pole9 slot89)
                (pole_region pole9 slot90)
                (pole_region pole9 slot91)
                (pole_position pole10 slot93)
                (pole_stop_moving pole10)
                (slot_have_pole slot93)
                (pole_available pole10)
                (pole_empty pole10)
                (pole_region pole10 slot91)
                (pole_region pole10 slot92)
                (pole_region pole10 slot93)
                (pole_region pole10 slot94)
                (pole_region pole10 slot95)
                (pole_region pole10 slot96)
                (pole_region pole10 slot97)
                (pole_region pole10 slot98)
                (pole_region pole10 slot99)
                (pole_position pole11 slot100)
                (pole_stop_moving pole11)
                (slot_have_pole slot100)
                (pole_available pole11)
                (pole_empty pole11)
                (pole_region pole11 slot99)
                (pole_region pole11 slot100)
                (pole_region pole11 slot101)
                (pole_region pole11 slot102)
                (pole_region pole11 slot103)
                (pole_region pole11 slot104)
                (pole_region pole11 slot105)
                (pole_region pole11 slot106)
                (pole_position gear1 slot49)
                (pole_available gear1)
                (pole_empty gear1)
                (pole_region gear1 slot49)
                (pole_region gear1 slot60)
                (pole_position gear2 slot106)
                (pole_available gear2)
                (pole_empty gear2)
                (pole_region gear2 slot106)
                (pole_region gear2 slot1)
                (forward_slot_connection slot1 slot2)
                (inverse_slot_connection slot2 slot1)
                (forward_slot_connection slot2 slot3)
                (inverse_slot_connection slot3 slot2)
                (forward_slot_connection slot3 slot4)
                (inverse_slot_connection slot4 slot3)
                (forward_slot_connection slot4 slot5)
                (inverse_slot_connection slot5 slot4)
                (forward_slot_connection slot5 slot6)
                (inverse_slot_connection slot6 slot5)
                (forward_slot_connection slot6 slot7)
                (inverse_slot_connection slot7 slot6)
                (forward_slot_connection slot7 slot8)
                (inverse_slot_connection slot8 slot7)
                (forward_slot_connection slot8 slot9)
                (inverse_slot_connection slot9 slot8)
                (forward_slot_connection slot9 slot10)
                (inverse_slot_connection slot10 slot9)
                (forward_slot_connection slot10 slot11)
                (inverse_slot_connection slot11 slot10)
                (forward_slot_connection slot11 slot12)
                (inverse_slot_connection slot12 slot11)
                (forward_slot_connection slot12 slot13)
                (inverse_slot_connection slot13 slot12)
                (forward_slot_connection slot13 slot14)
                (inverse_slot_connection slot14 slot13)
                (forward_slot_connection slot14 slot15)
                (inverse_slot_connection slot15 slot14)
                (forward_slot_connection slot15 slot16)
                (inverse_slot_connection slot16 slot15)
                (forward_slot_connection slot16 slot17)
                (inverse_slot_connection slot17 slot16)
                (forward_slot_connection slot17 slot18)
                (inverse_slot_connection slot18 slot17)
                (forward_slot_connection slot18 slot19)
                (inverse_slot_connection slot19 slot18)
                (forward_slot_connection slot19 slot20)
                (inverse_slot_connection slot20 slot19)
                (forward_slot_connection slot20 slot21)
                (inverse_slot_connection slot21 slot20)
                (forward_slot_connection slot21 slot22)
                (inverse_slot_connection slot22 slot21)
                (forward_slot_connection slot22 slot23)
                (inverse_slot_connection slot23 slot22)
                (forward_slot_connection slot23 slot24)
                (inverse_slot_connection slot24 slot23)
                (forward_slot_connection slot24 slot25)
                (inverse_slot_connection slot25 slot24)
                (forward_slot_connection slot25 slot26)
                (inverse_slot_connection slot26 slot25)
                (forward_slot_connection slot26 slot27)
                (inverse_slot_connection slot27 slot26)
                (forward_slot_connection slot27 slot28)
                (inverse_slot_connection slot28 slot27)
                (forward_slot_connection slot28 slot29)
                (inverse_slot_connection slot29 slot28)
                (forward_slot_connection slot29 slot30)
                (inverse_slot_connection slot30 slot29)
                (forward_slot_connection slot30 slot31)
                (inverse_slot_connection slot31 slot30)
                (forward_slot_connection slot31 slot32)
                (inverse_slot_connection slot32 slot31)
                (forward_slot_connection slot32 slot33)
                (inverse_slot_connection slot33 slot32)
                (forward_slot_connection slot33 slot34)
                (inverse_slot_connection slot34 slot33)
                (forward_slot_connection slot34 slot35)
                (inverse_slot_connection slot35 slot34)
                (forward_slot_connection slot35 slot36)
                (inverse_slot_connection slot36 slot35)
                (forward_slot_connection slot36 slot37)
                (inverse_slot_connection slot37 slot36)
                (forward_slot_connection slot37 slot38)
                (inverse_slot_connection slot38 slot37)
                (forward_slot_connection slot38 slot39)
                (inverse_slot_connection slot39 slot38)
                (forward_slot_connection slot39 slot40)
                (inverse_slot_connection slot40 slot39)
                (forward_slot_connection slot40 slot41)
                (inverse_slot_connection slot41 slot40)
                (forward_slot_connection slot41 slot42)
                (inverse_slot_connection slot42 slot41)
                (forward_slot_connection slot42 slot43)
                (inverse_slot_connection slot43 slot42)
                (forward_slot_connection slot43 slot44)
                (inverse_slot_connection slot44 slot43)
                (forward_slot_connection slot44 slot45)
                (inverse_slot_connection slot45 slot44)
                (forward_slot_connection slot45 slot46)
                (inverse_slot_connection slot46 slot45)
                (forward_slot_connection slot46 slot47)
                (inverse_slot_connection slot47 slot46)
                (forward_slot_connection slot47 slot48)
                (inverse_slot_connection slot48 slot47)
                (forward_slot_connection slot48 slot49)
                (inverse_slot_connection slot49 slot48)
                (forward_slot_connection slot49 slot60)
                (inverse_slot_connection slot60 slot49)
                (forward_slot_connection slot60 slot61)
                (inverse_slot_connection slot61 slot60)
                (forward_slot_connection slot61 slot62)
                (inverse_slot_connection slot62 slot61)
                (forward_slot_connection slot62 slot63)
                (inverse_slot_connection slot63 slot62)
                (forward_slot_connection slot63 slot64)
                (inverse_slot_connection slot64 slot63)
                (forward_slot_connection slot64 slot65)
                (inverse_slot_connection slot65 slot64)
                (forward_slot_connection slot65 slot66)
                (inverse_slot_connection slot66 slot65)
                (forward_slot_connection slot66 slot67)
                (inverse_slot_connection slot67 slot66)
                (forward_slot_connection slot67 slot68)
                (inverse_slot_connection slot68 slot67)
                (forward_slot_connection slot68 slot69)
                (inverse_slot_connection slot69 slot68)
                (forward_slot_connection slot69 slot70)
                (inverse_slot_connection slot70 slot69)
                (forward_slot_connection slot70 slot71)
                (inverse_slot_connection slot71 slot70)
                (forward_slot_connection slot71 slot72)
                (inverse_slot_connection slot72 slot71)
                (forward_slot_connection slot72 slot73)
                (inverse_slot_connection slot73 slot72)
                (forward_slot_connection slot73 slot74)
                (inverse_slot_connection slot74 slot73)
                (forward_slot_connection slot74 slot75)
                (inverse_slot_connection slot75 slot74)
                (forward_slot_connection slot75 slot76)
                (inverse_slot_connection slot76 slot75)
                (forward_slot_connection slot76 slot77)
                (inverse_slot_connection slot77 slot76)
                (forward_slot_connection slot77 slot78)
                (inverse_slot_connection slot78 slot77)
                (forward_slot_connection slot78 slot79)
                (inverse_slot_connection slot79 slot78)
                (forward_slot_connection slot79 slot80)
                (inverse_slot_connection slot80 slot79)
                (forward_slot_connection slot80 slot81)
                (inverse_slot_connection slot81 slot80)
                (forward_slot_connection slot81 slot82)
                (inverse_slot_connection slot82 slot81)
                (forward_slot_connection slot82 slot83)
                (inverse_slot_connection slot83 slot82)
                (forward_slot_connection slot83 slot84)
                (inverse_slot_connection slot84 slot83)
                (forward_slot_connection slot84 slot85)
                (inverse_slot_connection slot85 slot84)
                (forward_slot_connection slot85 slot86)
                (inverse_slot_connection slot86 slot85)
                (forward_slot_connection slot86 slot87)
                (inverse_slot_connection slot87 slot86)
                (forward_slot_connection slot87 slot88)
                (inverse_slot_connection slot88 slot87)
                (forward_slot_connection slot88 slot89)
                (inverse_slot_connection slot89 slot88)
                (forward_slot_connection slot89 slot90)
                (inverse_slot_connection slot90 slot89)
                (forward_slot_connection slot90 slot91)
                (inverse_slot_connection slot91 slot90)
                (forward_slot_connection slot91 slot92)
                (inverse_slot_connection slot92 slot91)
                (forward_slot_connection slot92 slot93)
                (inverse_slot_connection slot93 slot92)
                (forward_slot_connection slot93 slot94)
                (inverse_slot_connection slot94 slot93)
                (forward_slot_connection slot94 slot95)
                (inverse_slot_connection slot95 slot94)
                (forward_slot_connection slot95 slot96)
                (inverse_slot_connection slot96 slot95)
                (forward_slot_connection slot96 slot97)
                (inverse_slot_connection slot97 slot96)
                (forward_slot_connection slot97 slot98)
                (inverse_slot_connection slot98 slot97)
                (forward_slot_connection slot98 slot99)
                (inverse_slot_connection slot99 slot98)
                (forward_slot_connection slot99 slot100)
                (inverse_slot_connection slot100 slot99)
                (forward_slot_connection slot100 slot101)
                (inverse_slot_connection slot101 slot100)
                (forward_slot_connection slot101 slot102)
                (inverse_slot_connection slot102 slot101)
                (forward_slot_connection slot102 slot103)
                (inverse_slot_connection slot103 slot102)
                (forward_slot_connection slot103 slot104)
                (inverse_slot_connection slot104 slot103)
                (forward_slot_connection slot104 slot105)
                (inverse_slot_connection slot105 slot104)
                (forward_slot_connection slot105 slot106)
                (inverse_slot_connection slot106 slot105)
                (forward_slot_connection slot106 slot1)
                (inverse_slot_connection slot1 slot106)
                (exchanging_slot slot49)
                (exchanging_slot slot60)
                (exchanging_slot slot1)
                (exchanging_slot slot106)
                (exchanging_connection slot49 slot60)
                (exchanging_connection slot106 slot1)
                (exchanging_connection slot1 slot106)
                (exchanging_connection slot60 slot49)
                (= (pole_moving_duration_each_slot) 1)
                (= (pole_hangon_duration) 5)
                (= (pole_hangoff_duration) 5)
                (= (pole_start_duration) 2)
                (= (gear_moving_duration) 14)
        )
        (:goal
                (and
                )
        )
)