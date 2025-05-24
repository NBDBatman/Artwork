#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   GIMP - The GNU Image Manipulation Program
#   Copyright (C) 1995 Spencer Kimball and Peter Mattis
#
#   gimp-tutorial-plug-in.py
#   sample plug-in to illustrate the Python plug-in writing tutorial
#   Copyright (C) 2023 Jacob Boerema
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import os

from gi.repository import GLib
from gi.repository import GimpUi
from gi.repository import Gimp
from gi.repository import Gio

import gi
gi.require_version('Gimp', '3.0')
gi.require_version('GimpUi', '3.0')


class MyFirstPlugin (Gimp.PlugIn):
    def do_query_procedures(self):
        return ["fatalmerlin-plugin-export-ranks"]

    def do_set_i18n(self, name):
        return False

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.run, None)

        procedure.set_image_types("*")

        procedure.set_menu_label("Rank Exporter")
        procedure.add_menu_path('<Image>/Arkanis/')

        procedure.set_documentation("Arkanis Rank Exporter",
                                    "Exports the Arkanis Ranks to PNG",
                                    name)
        procedure.set_attribution("FatalMerlin", "Arkanis Corporation", "2023")

        return procedure

    def set_visible_recursively(self, layer, visible=True):
        layer.set_visible(visible)
        for child in layer.get_children():
            self.set_visible_recursively(child, visible)

    def show_all(self, image):
        for layer in image.get_layers():
            self.set_visible_recursively(layer)

    def hide_all(self, image):
        for layer in image.get_layers():
            self.set_visible_recursively(layer, False)

    def set_visible(self, image, layer_name, visible=True):
        layer = image.get_layer_by_name(layer_name)
        if layer is not None:
            layer.set_visible(visible)

    def export_to_png(self, image, image_name):
        export_path = '.export/' + ''.join(image_name) + ".png"
        Gimp.message(export_path)
        file = Gio.file_new_for_path(export_path)

        outdir = os.path.dirname(file)
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        Gimp.file_save(Gimp.RunMode.NONINTERACTIVE, image, file)

    def export_to_png2(self, image, export_path):
        file = Gio.file_new_for_path(export_path)

        pdb = Gimp.get_pdb()
        export_proc = pdb.lookup_procedure("file-png-export")
        config = export_proc.create_config()
        config.set_property("run-mode", Gimp.RunMode.NONINTERACTIVE)
        config.set_property("image", image)
        config.set_property("file", file)
        config.set_property("options", None)
        config.set_property("interlaced", False)
        config.set_property("compression", 1)
        config.set_property("bkgd", True)
        config.set_property("offs", False)
        config.set_property("phys", True)
        config.set_property("time", True)
        config.set_property("save-transparent", False)
        config.set_property("optimize-palette", False)
        config.set_property("format", "auto")
        config.set_property("include-exif", False)
        config.set_property("include-iptc", False)
        config.set_property("include-xmp", False)
        config.set_property("include-color-profile", False)
        config.set_property("include-thumbnail", True)
        config.set_property("include-comment", False)
        result = export_proc.run(config)

    def run(self, procedure, run_mode, image, drawables, config, run_data):

        try:
            image.undo_group_start()

            always_hide = ["Halo", "Background"]

            layers = [
                "200",
                "300",
                "010",
                "020",
                "030",
                "001",
                "002",
                "003",
            ]

            for layer_name in always_hide:
                self.set_visible(image, layer_name, False)

            for layer_name in layers:
                self.set_visible(image, layer_name, False)

            for index, layer_name in enumerate(layers):
                self.set_visible(image, layer_name)
                rank = str(index)

                self.export_to_png(image, rank)
                self.set_visible(image, "Halo")
                self.export_to_png(image, "Distinguished_" + rank)
                self.set_visible(image, "Halo", False)

        except Exception as e:
            Gimp.message("EXCEPTION: " + str(e))
            return procedure.new_return_values(Gimp.PDBStatusType.EXECUTION_ERROR, GLib.Error())

        # do what you want to do, then, in case of success, return:
        image.undo_group_end()
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())


Gimp.main(MyFirstPlugin.__gtype__, sys.argv)
