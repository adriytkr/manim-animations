from manim import *

class GridScene(MovingCameraScene):
  def setup(self):
    self.grid=NumberPlane(
      x_range=[-14,14,1],
      y_range=[-14,14,1]
    )
    self.camera.frame.scale(1.3)
    self.add(self.grid)

class Hook2DScene(GridScene):
  def construct(self):
    # Draw column space of matrix A
    basis_vec=Vector([4,1])
    basis_vec_normalized=basis_vec.get_end()/np.linalg.norm(basis_vec.get_end())
    basis_span=Line(
      start=-4*basis_vec.get_end(),
      end=4*basis_vec.get_end()
    )
    basis_span_label=MathTex(r'\text{col}(A)')
    basis_span_label.next_to(Dot([8,2,0]),DOWN)
    self.play(
      Create(basis_span),
      FadeIn(basis_span_label)
    )
    self.wait(0.5)

    # Samples
    def projection(vec:Vector,target:Vector)->Vector:
      vec_tip=vec.get_end()
      vec_arr=np.array([vec_tip[0],vec_tip[1]])

      target_tip=target.get_end()
      target_arr=np.array([target_tip[0],target_tip[1]])

      dp=np.dot(vec_arr,target_arr)
      proj_coords=(dp/np.linalg.norm(target_arr)**2)*target_arr
      return Vector(proj_coords)

    vec1=Vector([2,-2])
    vec2=Vector([6,-1])
    vec3=Vector([-6,2])
    vecs=[vec1,vec2,vec3]

    self.play(*[GrowArrow(vec) for vec in vecs])
    self.wait(0.5)

    self.play(*[Transform(vec,projection(vec,basis_vec)) for vec in vecs])
    self.wait(0.5)

    self.play(FadeOut(*vecs))
    self.wait(0.5)

    # Draw b
    b=Vector([2,3])
    b_label=MathTex(r'\vec b')
    b_label.next_to(b.get_end(),UP)
    self.play(
      GrowArrow(b),
      FadeIn(b_label)
    )
    self.wait(0.5)

    # Draw vectors evenly spaced on column space of A
    vecs=[Vector(-5*basis_vec_normalized*2+x*basis_vec_normalized*2) for x in range(12)]
    self.play(*[GrowArrow(vec) for vec in vecs])
    self.wait(0.5)

    self.play(*[FadeOut(vec) for vec in vecs])
    self.wait(0.5)

    # Distance vector
    t=ValueTracker(4)
    sample_vec=always_redraw(
      lambda:Vector(t.get_value()*basis_vec_normalized)
    )
    dist_vec=always_redraw(
      lambda:Vector(b.get_end()-sample_vec.get_end()).shift(sample_vec.get_end())
    )
    self.play(
      GrowArrow(sample_vec),
      GrowArrow(dist_vec)
    )
    self.wait(0.5)
    self.play(t.animate.set_value(8))
    self.wait(0.5)
    self.play(t.animate.set_value(-6))
    self.wait(0.5)
    x=projection(b,basis_vec)
    proj_b_basis_vec_norm=np.linalg.norm(x.get_end())
    self.play(t.animate.set_value(proj_b_basis_vec_norm))
    self.wait(0.5)

    # Subspaced that get mapped to the projection
    n_basis_span=(b.get_end()-x.get_end())
    n_basis_span=n_basis_span/np.linalg.norm(n_basis_span)
    n_span=Line(start=-10*n_basis_span,end=10*n_basis_span)
    n_span.shift(x.get_end())
    self.play(Create(n_span))
    self.wait(0.5)
    vecs=[Vector(n_basis_span*y*2+x.get_end()) for y in range(-5,5,1)]
    self.play(*[GrowArrow(vec) for vec in vecs])
    self.wait(0.5)

    self.play(*[Transform(vec,sample_vec) for vec in vecs])
    self.wait(0.5)
    self.remove(*vecs)

class Hook3DScene(ThreeDScene):
  def construct(self):
    self.set_camera_orientation(
      phi=75*DEGREES,
      theta=-75*DEGREES,
      # gamma=30*DEGREES,
      frame_center=self.camera.frame_center+RIGHT*2
    )
    axes=ThreeDAxes()
    axes.x_axis.set_opacity(0)
    axes.y_axis.set_opacity(0)
    self.add(axes)

    xy_plane=Surface(
      lambda u,v:np.array([u,v,0]),
      u_range=[-3,10],
      v_range=[-6,6],
      resolution=(20,20)
    )
    xy_plane.set_opacity(0.6)
    self.add(xy_plane)

    b=Arrow3D(start=ORIGIN,end=np.array([6,0,3]),thickness=0.02)
    self.play(GrowFromPoint(b,ORIGIN))
    self.wait(0.5)

    projection_b=Arrow3D(start=ORIGIN,end=[6,0,0],thickness=0.05)
    self.play(GrowFromPoint(projection_b,ORIGIN))
    self.wait(0.5)

    orthogonal_b=Arrow3D(start=[6,0,0],end=[6,0,3],thickness=0.05)
    self.play(GrowFromPoint(orthogonal_b,Point([6,0,0])))
    self.wait(0.5)

class ComputationPreliminaryScene(GridScene):
  def construct(self):
    # Draw column space of matrix A
    basis_vec=Vector([4,1])
    basis_vec_normalized=basis_vec.get_end()/np.linalg.norm(basis_vec.get_end())
    basis_span=Line(
      start=-4*basis_vec.get_end(),
      end=4*basis_vec.get_end()
    )
    basis_span_label=MathTex(r'\text{col}(A)')
    basis_span_label.next_to(Dot([8,2,0]),DOWN)
    self.play(
      Create(basis_span),
      FadeIn(basis_span_label)
    )
    self.wait(0.5)

    # Samples
    def projection(vec:Vector,target:Vector)->Vector:
      vec_tip=vec.get_end()
      vec_arr=np.array([vec_tip[0],vec_tip[1]])

      target_tip=target.get_end()
      target_arr=np.array([target_tip[0],target_tip[1]])

      dp=np.dot(vec_arr,target_arr)
      proj_coords=(dp/np.linalg.norm(target_arr)**2)*target_arr
      return Vector(proj_coords)

    # Draw b
    b=Vector([2,3])
    b_label=MathTex(r'\vec b')
    b_label.next_to(b.get_end(),UP)
    self.play(
      GrowArrow(b),
      FadeIn(b_label)
    )
    self.wait(0.5)

    # Draw b's projection onto column space of A
    b_projection=projection(b,basis_vec)
    b_projection_helper=DashedLine(
      start=b.get_end(),
      end=b_projection.get_end(),
      dash_length=0.2
    )
    self.play(Create(b_projection_helper))
    self.wait(0.5)
    self.play(GrowArrow(b_projection))
    self.wait(0.5)

class ComputationScene(Scene):
  def construct(self):
    eq1=MathTex(r'A\hat{x}','=',r'\text{proj}_{\text{col}(A)}b')
    eq2=MathTex('b','-',r'A\hat{x}','=','b','-',r'\text{proj}_{\text{col}(A)}b')
    eq3=MathTex(r'A^T','(','b','-',r'A\hat{x}',')','=','A^T','(','b','-',r'\text{proj}_{\text{col}(A)}b',')')
    eq4=MathTex(r'A^T','(','b','-',r'A\hat{x}',')','=','0')
    eq5=MathTex(r'A^T','b','-',r'A^T',r'A\hat{x}','=','0')
    eq6=MathTex(r'A^T','b','=',r'A^T',r'A\hat{x}')
    eqs=[eq1,eq2,eq3,eq4,eq5,eq6]

    self.play(Write(eq1))
    self.wait(0.5)
    for eq in range(len(eqs)-1):
      self.play(TransformMatchingTex(eqs[eq],eqs[eq+1]))
      self.wait(0.5)

    eq1.next_to(eqs[-1],DOWN)
    self.play(Write(eq1))
    self.play(VGroup(eq1,eqs[-1]).animate.move_to(ORIGIN))
    self.wait(0.5)
    eq1_reorg=MathTex(r'\text{proj}_{\text{col}(A)}b','=',r'A\hat{x}')
    eq1_reorg.move_to(eq1.get_center())
    self.play(TransformMatchingTex(eq1,eq1_reorg))
    self.wait(0.5)

class RightHandSideScene(Scene):
  def construct(self):
    eq1=MathTex('A','x','=','0')
    eq2=MathTex(r'\begin{pmatrix}r_1\\r_2\\\vdots\\r_n\end{pmatrix}','x','=','0')
    eq3=MathTex(
      r'r_1\cdot ','x',r'&=0\\',
      r'r_2\cdot ','x',r'&=0\\',
      r'\vdots\\',
      r'r_n\cdot ','x',r'&=0\\',
    )

    self.play(Write(eq1))
    self.wait(0.5)
    self.play(TransformMatchingTex(eq1,eq2))
    self.wait(0.5)
    self.play(TransformMatchingTex(eq2,eq3))
    self.wait(0.5)

    self.play(FadeOut(eq3))
    self.wait(0.5)

    eq4=MathTex(r'b-\text{proj}_{\text{col}(A)}b')
    eq5=MathTex(
      r'c_1\cdot ',r'b-\text{proj}_{\text{col}(A)}b',r'&=0\\',
      r'c_2\cdot ',r'b-\text{proj}_{\text{col}(A)}b',r'&=0\\',
      r'\vdots\\',
      r'c_n\cdot ',r'b-\text{proj}_{\text{col}(A)}b',r'&=0\\',
    )
    eq6=MathTex(
      r'\begin{pmatrix}c_1\\c_2\\\vdots\\c_n\end{pmatrix}',
      r'b-\text{proj}_{\text{col}(A)}b','=','0'
    )
    eq7=MathTex(
      r'A^T(',
      r'b-\text{proj}_{\text{col}(A)}b',
      ')','=','0'
    )

    self.play(Write(eq4))
    self.wait(0.5)
    self.play(TransformMatchingTex(eq4,eq5))
    self.wait(0.5)
    self.play(TransformMatchingTex(eq5,eq6))
    self.wait(0.5)
    self.play(TransformMatchingTex(eq6,eq7))

class RightHandSideHelperScene(GridScene):
  def construct(self):
    # Draw column space of matrix A
    basis_vec=Vector([4,1])
    basis_vec_normalized=basis_vec.get_end()/np.linalg.norm(basis_vec.get_end())
    basis_span=Line(
      start=-4*basis_vec.get_end(),
      end=4*basis_vec.get_end()
    )
    basis_span_label=MathTex(r'\text{col}(A)')
    basis_span_label.next_to(Dot([8,2,0]),DOWN)
    self.play(
      Create(basis_span),
      FadeIn(basis_span_label)
    )
    self.wait(0.5)

    # Samples
    def projection(vec:Vector,target:Vector)->Vector:
      vec_tip=vec.get_end()
      vec_arr=np.array([vec_tip[0],vec_tip[1]])

      target_tip=target.get_end()
      target_arr=np.array([target_tip[0],target_tip[1]])

      dp=np.dot(vec_arr,target_arr)
      proj_coords=(dp/np.linalg.norm(target_arr)**2)*target_arr
      return Vector(proj_coords)

    # Draw b
    b=Vector([2,3])
    b_label=MathTex(r'\vec b')
    b_label.next_to(b.get_end(),UP)
    self.play(
      GrowArrow(b),
      FadeIn(b_label)
    )
    self.wait(0.5)

    # Draw b's projection onto column space of A
    b_projection=projection(b,basis_vec)
    b_projection_helper=DashedLine(
      start=b.get_end(),
      end=b_projection.get_end(),
      dash_length=0.2
    )
    b_projection_label=MathTex(r'\text{proj}_{\text{col}(A)}b')
    b_projection_label.next_to(b_projection,DOWN)
    self.play(Create(b_projection_helper))
    self.wait(0.5)
    self.play(
      GrowArrow(b_projection),
      FadeIn(b_projection_label)
    )
    self.wait(0.5)

    orthogonal_comp=Vector(b.get_end()-b_projection.get_end())
    orthogonal_comp.shift(b_projection.get_end())
    orthogonal_comp_label=MathTex(r'b-\text{proj}_{\text{col}(A)}b')
    orthogonal_comp_label.next_to(orthogonal_comp,RIGHT)
    self.play(
      GrowArrow(orthogonal_comp),
      FadeIn(orthogonal_comp_label)
    )
    self.wait(0.5)
