bl_info = {
    "name": "PolyBake",
    "category": "3D View",
    "version": (1, 0, 1),
    "blender": (3, 00, 0),
    "author": "metarex21",
    "description": "Fast texture baking UI in 3D View Sidebar under 'bake'..",
    "website": "https://github.com/metarex21/PolyBake" 
}

import bpy
import os
import bmesh
from bpy.props import EnumProperty, BoolProperty, StringProperty, FloatProperty, IntProperty



def unhide(objectType):
    if objectType is None:
        for o in objectType.objects:
            o.hide_viewport = False
    else:
        objectType.hide_viewport = False

def hide(objectType):
    if objectType is None:
        for o in objectType.objects:
            o.hide_viewport = True
    else:
        objectType.hide_viewport = True


class PolyBakeUIPanel(bpy.types.Panel):
    """PolyBakeUIPanel Panel"""
    bl_label = "PolyBake"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "PolyBake"


    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='SCENE')

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        col = box.column(align=True)

        row = col.row(align = True)
        row.prop(context.scene, "lowpolyGroup", text="", icon="GROUP")
        if context.scene.lowpolyGroup is True:
            row.prop_search(context.scene, "lowpoly", bpy.data, "collections", text="", icon="MESH_ICOSPHERE")
        if context.scene.lowpolyGroup is False:
            row.prop_search(context.scene, "lowpoly", context.scene, "objects", text="", icon="MESH_ICOSPHERE")

            
        
        

        if context.scene.lowpolyActive is True:
            hideicon = "HIDE_OFF"
        if context.scene.lowpolyActive is False:
            hideicon = "HIDE_ON"
        op = row.operator("brm.bakeuihide", text="", icon=hideicon)
        op.targetmesh = "lowpoly"
        
        row = col.row(align = True)

        row.prop(context.scene, "hipolyGroup", text="", icon="GROUP")
        if context.scene.hipolyGroup is True:
            row.prop_search(context.scene, "hipoly", bpy.data, "collections", text="", icon="MESH_UVSPHERE")
        if context.scene.hipolyGroup is False:
            row.prop_search(context.scene, "hipoly", context.scene, "objects", text="", icon="MESH_UVSPHERE")

        row.enabled = not context.scene.UseLowOnly
        
        

        if context.scene.hipolyActive is True:
            hideicon = "HIDE_OFF"
        if context.scene.hipolyActive is False:
            hideicon = "HIDE_ON"
        op = row.operator("brm.bakeuihide", text="", icon=hideicon)
        op.targetmesh = "hipoly"

        

        col = box.column(align=True)
        row = col.row(align = True)
        row.operator("brm.bakeuitoggle", text="Toggle hi/low", icon="FILE_REFRESH")
        

        col = layout.column(align=True)

        col.separator()
        row = col.row(align = True)
        row.prop(context.scene.render.bake, "cage_extrusion", text="Ray Distance")
        
        row = col.row(align = True)
       
        col.separator()

        box = layout.box()
        col = box.column(align=True)

        row = col.row(align = True)
        row.label(text="Width:")
        row.operator("brm.bakeuiincrement", text="", icon="REMOVE").target = "width/2"
        row.prop(context.scene, "bakeWidth", text="")
        row.operator("brm.bakeuiincrement", text="", icon="ADD").target = "width*2"
        
        row = col.row(align = True)
        row.label(text="Height:")
        row.operator("brm.bakeuiincrement", text="", icon="REMOVE").target = "height/2"
        row.prop(context.scene, "bakeHeight", text="")
        row.operator("brm.bakeuiincrement", text="", icon="ADD").target = "height*2"
        row = col.row(align = True)
        row.label(text="Padding:")
        row.prop(context.scene.render.bake, "margin", text="")
        
        

        col = layout.column(align=True)
        col.separator()
        col.prop(context.scene, 'bakeFolder', text="")
        row = col.row(align = True)
        row.label(text="Filename:")
        row.prop(context.scene, "bakePrefix", text="")
        
        col.separator()

        box = layout.box()
        col = box.column(align=True)
        
        row = col.row(align = True)
        
        
        if not context.scene.bakeNormal:
            row.prop(context.scene, "bakeNormal", icon="SHADING_RENDERED", text="Tangent Normal")
        if context.scene.bakeNormal:
            row.prop(context.scene, "bakeNormal", icon="SHADING_RENDERED", text=" ")
            row.prop(context.scene, "affixNormal", text="")
            row.prop(context.scene, "samplesNormal", text="")

        row = col.row(align = True)
        
        if not context.scene.bakeObject:
            row.prop(context.scene, "bakeObject", icon="SHADING_RENDERED", text="Object Normal")
        if context.scene.bakeObject:
            row.prop(context.scene, "bakeObject", icon="SHADING_RENDERED", text=" ")
            row.prop(context.scene, "affixObject", text="")
            row.prop(context.scene, "samplesObject", text="")
            
        row = col.row(align = True)
        if not context.scene.bakeAO:
            row.prop(context.scene, "bakeAO", icon="SHADING_SOLID", text="Occlusion")
        if context.scene.bakeAO:
            row.prop(context.scene, "bakeAO", icon="SHADING_SOLID", text=" ")
            row.prop(context.scene, "affixAO", text="")
            row.prop(context.scene, "samplesAO", text="")
        
        row = col.row(align = True)
        
        if not context.scene.bakeColor:
            row.prop(context.scene, "bakeColor", icon="SHADING_TEXTURE", text="Color")
        if context.scene.bakeColor:
            row.prop(context.scene, "bakeColor", icon="SHADING_TEXTURE", text=" ")
            row.prop(context.scene, "affixColor", text="")
            row.prop(context.scene, "samplesColor", text="")

        row = col.row(align = True)
        
        if not context.scene.bakeRoughness:
            row.prop(context.scene, "bakeRoughness", icon="SHADING_TEXTURE", text="Roughness")
        if context.scene.bakeRoughness:
            row.prop(context.scene, "bakeRoughness", icon="SHADING_TEXTURE", text=" ")
            row.prop(context.scene, "affixRoughness", text="")
            row.prop(context.scene, "samplesRoughness", text="")
            
        row = col.row(align = True)
        
        if not context.scene.bakeEmission:
            row.prop(context.scene, "bakeEmission", icon="SHADING_TEXTURE", text="Emission")
        if context.scene.bakeEmission:
            row.prop(context.scene, "bakeEmission", icon="SHADING_TEXTURE", text=" ")
            row.prop(context.scene, "affixEmission", text="")
            row.prop(context.scene, "samplesEmission", text="")
            row.prop(context.scene, "bakeEmissionLinear", icon="NODE_TEXTURE", text="")

        row = col.row(align = True)
        if not context.scene.bakeUV:
            row.prop(context.scene, "bakeUV", icon="SHADING_WIRE", text="UV Snapshot")
        if context.scene.bakeUV:
            row.prop(context.scene, "bakeUV", icon="SHADING_WIRE", text=" ")
            row.prop(context.scene, "affixUV", text="")
            row.prop(context.scene, "bakeUV", icon="BLANK1", text=" ")
            
        
        col = layout.column(align=True)
        col.separator()
        row = col.row(align = True)
        op = row.operator("brm.bake", text="Bake!", icon="RENDER_RESULT")
        row.prop(context.scene, "UseLowOnly", icon="MESH_ICOSPHERE", text="")
        

class PolyBakeUIToggle(bpy.types.Operator):
    """toggle lowpoly/hipoly"""
    bl_idname = "brm.bakeuitoggle"
    bl_label = "Toggle"
    bl_options = {"UNDO"}

    def execute(self, context):

        if bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')

        

        if context.scene.lowpoly is None and not context.scene.lowpoly in bpy.data.collections:
            self.report({'WARNING'}, "Select a valid lowpoly object or group!")
            return {'FINISHED'}
        if context.scene.hipoly is None and not context.scene.hipoly in bpy.data.collections:
            self.report({'WARNING'}, "Select a valid hipoly object or group!")
            return {'FINISHED'}

        if context.scene.lowpolyActive is True:
            context.scene.lowpolyActive = False
            hide(context.scene.lowpoly)
            context.scene.hipolyActive = True
            unhide(context.scene.hipoly)
        else:
            context.scene.lowpolyActive = True
            unhide(context.scene.lowpoly)
            context.scene.hipolyActive = False
            hide(context.scene.hipoly)

        return {'FINISHED'}



class PolyBakeUIIncrement(bpy.types.Operator):
    """multiply/divide value"""
    bl_idname = "brm.bakeuiincrement"
    bl_label = "increment"

    target : bpy.props.StringProperty()

    def execute(self, context):
        if self.target == "width/2" and context.scene.bakeWidth > 4:
            context.scene.bakeWidth = context.scene.bakeWidth // 2
        if self.target == "width*2":
            context.scene.bakeWidth = context.scene.bakeWidth * 2
        if self.target == "height/2" and context.scene.bakeHeight > 4:
            context.scene.bakeHeight = context.scene.bakeHeight // 2
        if self.target == "height*2":
            context.scene.bakeHeight = context.scene.bakeHeight * 2
        return {'FINISHED'}



class PolyBakeUIHide(bpy.types.Operator):
    """hide object"""
    bl_idname = "brm.bakeuihide"
    bl_label = "hide"
    bl_options = {"UNDO"}

    targetmesh : bpy.props.StringProperty()

    def execute(self, context):


        
        if context.scene.hipoly.bl_rna.name == "Collection":
            print("i am a collection!")

        if context.scene.hipoly.bl_rna.name == "Object":
            print("i am an object!")
        
        

        
        if bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        

        if self.targetmesh == "lowpoly":

            if context.scene.lowpoly is None and not context.scene.lowpoly in bpy.data.collections:
                self.report({'WARNING'}, "Select a valid lowpoly object or collection!")
                return {'FINISHED'}

            else:
                if context.scene.lowpolyActive is True:
                    context.scene.lowpolyActive = False
                    hide(context.scene.lowpoly)
                else:
                    context.scene.lowpolyActive = True
                    unhide(context.scene.lowpoly)

        if self.targetmesh == "hipoly":
            
            if context.scene.hipoly is None and not context.scene.hipoly in bpy.data.collections:
                self.report({'WARNING'}, "Select a valid hipoly object or collection!")
                return {'FINISHED'}

            else:
                if context.scene.hipolyActive is True:
                    context.scene.hipolyActive = False
                    hide(context.scene.hipoly)
                else:
                    context.scene.hipolyActive = True
                    unhide(context.scene.hipoly)

        return {'FINISHED'}



class PolyBake(bpy.types.Operator):
    """Bake and save textures"""
    bl_idname = "brm.bake"
    bl_label = "set normal"
    bl_options = {"UNDO"}
    

    def execute(self, context):  
        
        
        
        hasfolder = os.access(context.scene.bakeFolder, os.W_OK)
        if hasfolder is False:
            self.report({'WARNING'}, "Select a valid export folder!")
            return {'FINISHED'}

        
        
        
        if context.scene.lowpoly is None and not context.scene.lowpoly in bpy.data.collections:
            self.report({'WARNING'}, "Select a valid lowpoly object or collection!")
            return {'FINISHED'}
            
        if context.scene.hipoly is None and not context.scene.hipoly in bpy.data.collections and not context.scene.UseLowOnly:
            self.report({'WARNING'}, "Select a valid hipoly object or collection!")
            return {'FINISHED'}
            
        
     
        lowpolymeshes = 0

        if context.scene.lowpolyGroup == True:
            for o in bpy.context.scene.lowpoly.all_objects:
                if o.type == 'MESH':
                    lowpolymeshes+=1
        else:
            if context.scene.lowpoly.type == 'MESH':
                lowpolymeshes = 1
        if lowpolymeshes == 0:
            self.report({'WARNING'}, "lowpoly needs to have a mesh!")
            return {'FINISHED'}   
        
        
        
        if not context.scene.UseLowOnly:
            hipolymeshes = 0
            if context.scene.hipolyGroup == True:
                for o in bpy.context.scene.hipoly.all_objects:
                    if o.type == 'MESH':
                        hipolymeshes+=1
            else:
                if context.scene.hipoly.type == 'MESH':
                    hipolymeshes = 1
            if hipolymeshes == 0:
                self.report({'WARNING'}, "hipoly needs to have a mesh!")
                return {'FINISHED'}
        
        if context.scene.cageEnabled and bpy.data.objects[context.scene.cage].type != 'MESH':
            self.report({'WARNING'}, "cage needs to be a mesh!")
            return {'FINISHED'}

        
        

    
        if context.space_data.local_view:
            bpy.ops.view3d.localview()

    
        if not context.scene.UseLowOnly:
            unhide(context.scene.hipoly)
        unhide(context.scene.lowpoly)
        bpy.ops.object.hide_view_clear() 
        
        
        
    
        if bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        
        

    
        lowpolyobject = "null"
        orig_lowpoly = None
        
        
        
        
        
        if context.scene.lowpolyGroup == True:

            
            
            context.scene.lowpoly.hide_render = False

            
            low_objects_names = [obj.name for obj in bpy.context.scene.lowpoly.all_objects]
            for o in low_objects_names:
    
        
 
                if bpy.data.objects[o].type == 'MESH':
                    
                    

                    bpy.data.objects[o].hide_viewport = False    
                    
                    bpy.data.objects[o].select_set(state=True)
                    
                    context.view_layer.objects.active = bpy.data.objects[o]
                    
                    bpy.data.objects[o].hide_render = True
                    
            
            

            
            
            
            bpy.ops.object.duplicate()
            bpy.ops.object.join()
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
            lowpolyobject = bpy.context.selected_objects[0].name
            bpy.data.objects[lowpolyobject].hide_render = False
        else:
            bpy.ops.object.select_all(action='DESELECT')
            
            
            context.scene.lowpoly.hide_viewport = False
            context.scene.lowpoly.hide_render = False
            context.scene.lowpoly.select_set(state=True)
            
            orig_lowpoly = context.scene.lowpoly
            lowpolyobject = context.scene.lowpoly
            
        
        
            
    
        if context.scene.UseLowOnly:
            bpy.ops.object.duplicate()
            bpy.context.active_object.name = "temp_hipoly"
            context.scene.hipoly = bpy.context.active_object
            

    
        if context.scene.cageEnabled:
            vcount_low = len(bpy.data.objects[lowpolyobject].data.vertices)
            vcount_cage = len(bpy.data.objects[context.scene.cage].data.vertices)
            if vcount_low != vcount_cage:
                if context.scene.lowpolyGroup:
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.data.objects[lowpolyobject].select_set(state=True)
                    bpy.ops.object.delete(use_global=False)
                self.report({'WARNING'}, "cage and low poly vertex count don't match!")
                return {'FINISHED'}

    
        orig_renderer = bpy.data.scenes[bpy.context.scene.name].render.engine
        bpy.data.scenes[bpy.context.scene.name].render.engine = "CYCLES"

    
        bakeimage = bpy.data.images.new("BakeImage", width=context.scene.bakeWidth, height=context.scene.bakeHeight)
        bakemat = bpy.data.materials.new(name="bakemat")
        bakemat.use_nodes = True
        
    
        
        
        if context.scene.hipoly.bl_rna.name == "Collection":
            context.scene.hipoly.hide_render = False
            for o in bpy.context.scene.hipoly.all_objects:
                if o.type == 'MESH':
                    o.hide_viewport = False
                    o.hide_render = False
                    o.select_set(state=True)
        else:
            context.scene.hipoly.hide_viewport = False
            context.scene.hipoly.hide_render = False

            context.scene.hipoly.select_set(state=True)

    
        print("whats happening here?")
        print(context.scene.lowpoly)
        print(lowpolyobject)
        
        
        if context.scene.lowpolyGroup == True:
            bpy.context.view_layer.objects.active = bpy.data.objects[lowpolyobject]
        else:
            bpy.context.view_layer.objects.active = lowpolyobject

    
        orig_mat = bpy.context.active_object.data.materials[0]
        bpy.context.active_object.data.materials[0] = bakemat
        node_tree = bakemat.node_tree
        node = node_tree.nodes.new("ShaderNodeTexImage")
        node.select = True
        node_tree.nodes.active = node
        node.image = bakeimage

    
        if context.scene.cageEnabled:
            bpy.context.scene.render.bake.use_cage = True
            bpy.context.scene.render.bake.cage_object = bpy.data.objects[context.scene.cage]
        else:
            bpy.context.scene.render.bake.use_cage = False


        if context.scene.bakeNormal:

            bpy.context.scene.cycles.samples = context.scene.samplesNormal
            bpy.ops.object.bake(type='NORMAL', use_clear=True, use_selected_to_active=True, normal_space='TANGENT')
            bakeimage.filepath_raw = context.scene.bakeFolder+context.scene.bakePrefix+context.scene.affixNormal+".tga"
            bakeimage.file_format = 'TARGA'
            bakeimage.save()
        
        if context.scene.bakeObject:

            bpy.context.scene.cycles.samples = context.scene.samplesObject
            bpy.ops.object.bake(type='NORMAL', use_clear=True, use_selected_to_active=True, normal_space='OBJECT')
            bakeimage.filepath_raw = context.scene.bakeFolder+context.scene.bakePrefix+context.scene.affixObject+".tga"
            bakeimage.file_format = 'TARGA'
            bakeimage.save()

        if context.scene.bakeAO:

            bpy.context.scene.cycles.samples = context.scene.samplesAO
            bpy.ops.object.bake(type='AO', use_clear=True, use_selected_to_active=True)
            bakeimage.filepath_raw = context.scene.bakeFolder+context.scene.bakePrefix+context.scene.affixAO+".tga"
            bakeimage.file_format = 'TARGA'
            bakeimage.save()

        if context.scene.bakeColor:

            bpy.context.scene.cycles.samples = context.scene.samplesColor
            bpy.context.scene.render.bake.use_pass_direct = False
            bpy.context.scene.render.bake.use_pass_indirect = False
            bpy.context.scene.render.bake.use_pass_color = True
            bpy.ops.object.bake(type='DIFFUSE', use_clear=True, use_selected_to_active=True)
            bakeimage.filepath_raw = context.scene.bakeFolder+context.scene.bakePrefix+context.scene.affixColor+".tga"
            bakeimage.file_format = 'TARGA'
            bakeimage.save()
        
        if context.scene.bakeRoughness:

            bakeimage.colorspace_settings.name="Non-Color"

            bpy.context.scene.cycles.samples = context.scene.samplesRoughness
            bpy.ops.object.bake(type='ROUGHNESS', use_clear=True, use_selected_to_active=True)
            bakeimage.filepath_raw = context.scene.bakeFolder+context.scene.bakePrefix+context.scene.affixRoughness+".tga"
            bakeimage.file_format = 'TARGA'
            bakeimage.save()
            
        if context.scene.bakeEmission:

            bpy.context.scene.cycles.samples = context.scene.samplesEmission
            
            print("colorspace")
            print(bakeimage.colorspace_settings.name)
            
            if context.scene.bakeEmissionLinear:
                bakeimage.colorspace_settings.name="Linear"
            
            bpy.ops.object.bake(type='EMIT', use_clear=True, use_selected_to_active=True)
            bakeimage.filepath_raw = context.scene.bakeFolder+context.scene.bakePrefix+context.scene.affixEmission+".tga"
            bakeimage.file_format = 'TARGA'
            bakeimage.save()

        
        if context.scene.bakeUV:
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.object.editmode_toggle()
            original_type = bpy.context.area.type
            bpy.context.area.type = "IMAGE_EDITOR"
            uvfilepath = context.scene.bakeFolder+context.scene.bakePrefix+context.scene.affixUV+".png"
            bpy.ops.uv.export_layout(filepath=uvfilepath, size=(context.scene.bakeWidth, context.scene.bakeHeight))
            bpy.context.area.type = original_type



        
        bpy.ops.object.select_all(action='DESELECT')
        if not context.scene.lowpolyGroup:
            orig_lowpoly.select_set(state=True)
        bpy.data.images.remove(bakeimage)
        bakemat.node_tree.nodes.remove(node)
        bpy.data.materials.remove(bakemat)
        bpy.context.active_object.data.materials[0] = orig_mat
        bpy.data.scenes[bpy.context.scene.name].render.engine = orig_renderer

        if context.scene.lowpolyGroup:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[lowpolyobject].select_set(state=True)
            bpy.ops.object.delete(use_global=False)
            
        if context.scene.UseLowOnly:
            
            context.scene.hipoly.select_set(state=True)
            
            bpy.ops.object.delete(use_global=False)
            

        
        for image in bpy.data.images:
            image.reload()
             

        
        if context.scene.lowpolyActive is True:
            if context.scene.lowpoly is None:
                for o in context.scene.lowpoly.objects:
                    o.hide_viewport = False
                    context.view_layer.objects.active = o
            else:
                context.scene.lowpoly.hide_viewport = False
                


        else:
            if context.scene.lowpoly is None:
                for o in context.scene.lowpoly.objects:
                    o.hide_viewport = True
            else:
                context.scene.lowpoly.hide_viewport = True

        if not context.scene.UseLowOnly:
            if context.scene.hipolyActive is True:
                if context.scene.hipoly is None:
                    for o in context.scene.hipoly.objects:
                        o.hide_viewport = False
                        context.view_layer.objects.active = o
                else:
                    context.scene.hipoly.hide_viewport = False
                    context.view_layer.objects.active =context.scene.hipoly
            else:
                if context.scene.hipoly is None:
                    for o in context.scene.hipoly.objects:
                        o.hide_viewport = True
                else:
                    context.scene.hipoly.hide_viewport = True

        return {'FINISHED'}




classes = (
        PolyBake,
        PolyBakeUIHide,
        PolyBakeUIPanel,
        PolyBakeUIToggle,
        PolyBakeUIIncrement,
    )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.lowpoly = bpy.props.PointerProperty (name = "lowpoly",  type=bpy.types.Object, description = "lowpoly object")
    bpy.types.Scene.lowpolyActive = bpy.props.BoolProperty (name = "lowpolyActive", default = True, description = "lowpolyActive")
    bpy.types.Scene.lowpolyGroup = bpy.props.BoolProperty (name = "lowpolyGroup",default = False,description = "enable lowpoly collection")
    bpy.types.Scene.hipoly = bpy.props.PointerProperty (name = "hipoly",type=bpy.types.Object,description = "hipoly object or group")
    bpy.types.Scene.hipolyActive = bpy.props.BoolProperty (name = "hipolyActive",default = True,description = "hipolyActive")
    bpy.types.Scene.hipolyGroup = bpy.props.BoolProperty (name = "hipolyGroup",default = False,description = "enable hipoly collection")
    bpy.types.Scene.cage = bpy.props.StringProperty (name = "cage",default = "cage",description = "cage object")
    bpy.types.Scene.cageActive = bpy.props.BoolProperty (name = "cageActive",default = True,description = "cageActive")
    bpy.types.Scene.cageEnabled = bpy.props.BoolProperty (name = "cageEnabled",default = False,description = "Enable cage object for baking")
    
    bpy.types.Scene.bakeNormal = bpy.props.BoolProperty (name = "bakeNormal",default = False,description = "Bake Tangent Space Normal Map")
    bpy.types.Scene.bakeObject = bpy.props.BoolProperty (name = "bakeObject",default = False,description = "Bake Object Space Normal Map")
    bpy.types.Scene.bakeAO = bpy.props.BoolProperty (name = "bakeAO",default = False,description = "Bake Ambient Occlusion Map")
    bpy.types.Scene.bakeColor = bpy.props.BoolProperty (name = "bakeColor",default = False,description = "Bake Albedo Color Map")
    bpy.types.Scene.bakeRoughness = bpy.props.BoolProperty (name = "bakeRoughness",default = False,description = "Bake Roughness Map")
    bpy.types.Scene.bakeEmission = bpy.props.BoolProperty (name = "bakeEmission",default = False,description = "Bake Emission Map") 
    bpy.types.Scene.bakeEmissionLinear = bpy.props.BoolProperty (name = "bakeEmissionLinear",default = False,description = "Use Linear") 
    bpy.types.Scene.bakeUV = bpy.props.BoolProperty (name = "bakeUV",default = False,description = "Bake UV Wireframe Snapshot of Lowpoly Mesh")
    
    bpy.types.Scene.samplesNormal = bpy.props.IntProperty (name = "samplesNormal",default = 8,description = "Tangent Space Normal Map Sample Count")
    bpy.types.Scene.samplesObject = bpy.props.IntProperty (name = "samplesObject",default = 8,description = "Object Space Normal Map Sample Count")
    bpy.types.Scene.samplesAO = bpy.props.IntProperty (name = "samplesAO",default = 128,description = "Ambient Occlusion Map Sample Count")
    bpy.types.Scene.samplesColor = bpy.props.IntProperty (name = "samplesColor",default = 1,description = "Color Map Sample Count")
    bpy.types.Scene.samplesEmission = bpy.props.IntProperty (name = "samplesEmission",default = 1,description = "Emission Map Sample Count")
    bpy.types.Scene.samplesRoughness = bpy.props.IntProperty (name = "samplesRoughness",default = 1,description = "Roughness Map Sample Count")
    
    bpy.types.Scene.bakeWidth = bpy.props.IntProperty (name = "bakeWidth",default = 512,description = "Export Texture Width")  
    bpy.types.Scene.bakeHeight = bpy.props.IntProperty (name = "bakeHeight",default = 512,description = "Export Texture Height")
    bpy.types.Scene.bakePrefix = bpy.props.StringProperty (name = "bakePrefix",default = "export",description = "export filename")
    bpy.types.Scene.bakeFolder = bpy.props.StringProperty (name = "bakeFolder",default = "C:\\export\\",description = "destination folder",subtype = 'DIR_PATH')
    bpy.types.Scene.UseLowOnly = bpy.props.BoolProperty (name = "UseLowOnly",default = False,description = "Only bake lowpoly on itself")
    
    bpy.types.Scene.affixNormal = bpy.props.StringProperty (name = "affixNormal",default = "_normal",description = "normal map affix")
    bpy.types.Scene.affixObject = bpy.props.StringProperty (name = "affixObject",default = "_object",description = "object normal map affix")
    bpy.types.Scene.affixAO = bpy.props.StringProperty (name = "affixAO",default = "_ao",description = "AO map affix")
    bpy.types.Scene.affixColor = bpy.props.StringProperty (name = "affixColor",default = "_color",description = "color map affix")
    bpy.types.Scene.affixRoughness = bpy.props.StringProperty (name = "affixRoughness",default = "_rough",description = "Roughness map affix")
    bpy.types.Scene.affixEmission = bpy.props.StringProperty (name = "affixEmission",default = "_emit",description = "Emission map affix")
    bpy.types.Scene.affixUV = bpy.props.StringProperty (name = "affixUV",default = "_uv",description = "UV map affix")


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    
if __name__ == "__main__":
    register()
