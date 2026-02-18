from manim import *

class GridScene(MovingCameraScene):
  def setup(self):
    self.grid=NumberPlane(
      x_range=[-14,14,1],
      y_range=[-14,14,1]
    )
    self.camera.frame.scale(1.3)
    self.add(self.grid)
  def projection(self,vec:Vector,target:Vector)->Vector:
    vec_tip=vec.get_end()
    vec_arr=np.array([vec_tip[0],vec_tip[1]])

    target_tip=target.get_end()
    target_arr=np.array([target_tip[0],target_tip[1]])

    dp=np.dot(vec_arr,target_arr)
    proj_coords=(dp/np.linalg.norm(target_arr)**2)*target_arr
    return Vector(proj_coords)

class Hook2DScene(GridScene):
  def construct(self):
    # Draw column space of matrix A
    basis_vec=Vector([4,1])
    basis_vec_normalized=basis_vec.get_end()/np.linalg.norm(basis_vec.get_end())
    basis_vec_span=Line(
      start=-4*basis_vec.get_end(),
      end=4*basis_vec.get_end()
    )
    basis_vec_span_label=MathTex(r'\text{col}(A)')
    basis_vec_span_label.next_to(Dot([8,2,0]),DOWN)

    self.play(
      Create(basis_vec_span),
      FadeIn(basis_vec_span_label)
    )
    self.wait(0.5)

    # Draw samples
    vecs=[
      Vector([2,-2]),
      Vector([6,-1]),
      Vector([-6,2])
    ]

    self.play(*[GrowArrow(vec) for vec in vecs])
    self.wait(0.5)
    self.play(*[Transform(vec,self.projection(vec,basis_vec)) for vec in vecs])
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
    vecs=[Vector(basis_vec_normalized*2*x) for x in range(-5,6,1)]

    self.play(*[GrowArrow(vec) for vec in vecs])
    self.wait(0.5)
    self.play(*[FadeOut(vec) for vec in vecs])
    self.wait(0.5)

    # Distance vector
    t=ValueTracker(0)
    sample_vec=always_redraw(
      lambda:Vector(t.get_value()*basis_vec_normalized)
    )
    dist_vec=always_redraw(
      lambda:Vector(b.get_end()-sample_vec.get_end()).shift(sample_vec.get_end())
    )
    proj_b_on_colA=self.projection(b,basis_vec)
    proj_b_on_colA_label=MathTex(r'\text{proj}_{\text{col}(A)}b')

    self.add(sample_vec,dist_vec)
    self.wait(0.5)
    self.play(t.animate.set_value(8))
    self.wait(0.5)
    self.play(t.animate.set_value(-6))
    self.wait(0.5)
    self.play(t.animate.set_value(np.linalg.norm(proj_b_on_colA.get_end())))
    proj_b_on_colA_label.next_to(dist_vec.get_start(),DOWN*2)
    self.play(FadeIn(proj_b_on_colA_label))
    self.wait(0.5)

    # Subspaced that get mapped to the projection
    m_basis_vec=(b.get_end()-proj_b_on_colA.get_end())
    m_basis_vec=m_basis_vec/np.linalg.norm(m_basis_vec)
    m_basis_vec_span=Line(
      start=-10*m_basis_vec,
      end=10*m_basis_vec
    )
    m_basis_vec_span.shift(proj_b_on_colA.get_end())
    vecs=[Vector(m_basis_vec*y*2+proj_b_on_colA.get_end()) for y in range(-5,5,1)]

    self.wait(0.5)
    self.play(
      FadeOut(sample_vec,proj_b_on_colA_label),
      Create(m_basis_vec_span)
    )
    self.wait(0.5)
    self.play(*[GrowArrow(vec) for vec in vecs])
    self.wait(0.5)
    self.play(*[Transform(vec,sample_vec) for vec in vecs])
    self.wait(0.5)
    self.remove(*vecs)

class Hook3DScene(ThreeDScene):
  def construct(self):
    self.wait(0.5)
    self.set_camera_orientation(
      phi=75*DEGREES,
      theta=-75*DEGREES,
      frame_center=self.camera.frame_center+RIGHT*2
    )

    # Create axis
    axes=ThreeDAxes()
    axes.x_axis.set_opacity(0)
    axes.y_axis.set_opacity(0)
    self.add(axes)

    # Create plane
    xy_plane=Surface(
      lambda u,v:np.array([u,v,0]),
      u_range=[-3,10],
      v_range=[-6,6],
      resolution=(20,20)
    )
    xy_plane.set_opacity(0.6)
    self.play(Create(xy_plane))

    # Draw b
    b=Arrow3D(start=ORIGIN,end=np.array([6,0,3]),thickness=0.02)
    self.play(GrowFromPoint(b,ORIGIN))
    self.wait(0.5)

    # Draw samples
    tx=ValueTracker(4)
    ty=ValueTracker(3)
    sample_vec=always_redraw(
      lambda:Arrow3D(
        start=ORIGIN,
        end=[tx.get_value(),ty.get_value(),0],
        thickness=0.05
      )
    )
    dist_vec=always_redraw(
      lambda:Arrow3D(
        start=sample_vec.get_end(),
        end=b.get_end(),
        thickness=0.05
      )
    )

    self.play(
      GrowFromPoint(sample_vec,ORIGIN),
      GrowFromPoint(dist_vec,ORIGIN)
    )
    self.play(tx.animate.set_value(9))
    self.play(
      tx.animate.set_value(5),
      ty.animate.set_value(-4)
    )
    self.play(
      tx.animate.set_value(-2),
      ty.animate.set_value(4)
    )
    self.play(
      tx.animate.set_value(1),
      ty.animate.set_value(-4)
    )
    self.play(
      tx.animate.set_value(6),
      ty.animate.set_value(0)
    )

class ComputationScene(Scene):
  def construct(self):
    # Equations
    tmp=[
      r'A\hat{x}','=',
      r'\text{proj}_{\text{col}(A)}b'
    ]
    eq1=MathTex(*tmp)
    eq1_reorg=MathTex(*tmp[::-1])
    eq2=MathTex(
      'b','-',r'A\hat{x}','=',
      'b','-',r'\text{proj}_{\text{col}(A)}b'
    )
    eq3=MathTex(
      r'A^T','(','b','-',r'A\hat{x}',')','=',
      'A^T','(','b','-',r'\text{proj}_{\text{col}(A)}b',')'
    )
    eq4=MathTex(r'A^T','(','b','-',r'A\hat{x}',')','=','0')
    eq5=MathTex(r'A^T','b','-',r'A^T',r'A\hat{x}','=','0')
    eq6=MathTex(r'A^T','b','=',r'A^T',r'A\hat{x}')
    eqs=[eq1,eq2,eq3,eq4,eq5,eq6]

    self.play(Write(eq1))
    self.wait(0.5)
    for x in range(len(eqs)-1):
      self.play(TransformMatchingTex(eqs[x],eqs[x+1]))
      self.wait(0.5)
    self.play(Indicate(eqs[-1]))
    self.wait(0.5)
    eq1.next_to(eqs[-1],DOWN)
    self.play(Write(eq1))
    eq1_reorg.move_to(eq1.get_center())
    self.play(TransformMatchingTex(eq1,eq1_reorg))
    self.wait(0.5)
    self.play(VGroup(eq1_reorg,eqs[-1]).animate.move_to(ORIGIN))
    self.wait(0.5)

class RightHandSideScene(Scene):
  def construct(self):
    self.wait(0.5)

    # General
    eq_init=MathTex('b','-',r'\text{proj}_{\text{col}(A)}b')
    self.play(Write(eq_init))
    self.wait(0.5)
    self.play(FadeOut(eq_init))
    self.wait(0.5)

    eq1=MathTex('A','x','=','0')
    eq2=MathTex(r'\begin{pmatrix}r_1\\r_2\\\vdots\\r_n\end{pmatrix}','x','=','0')
    eq3=MathTex(
      r'r_1\cdot ','x',r'&=0\\',
      r'r_2\cdot ','x',r'&=0\\',
      r'\vdots\\',
      r'r_n\cdot ','x',r'&=0\\',
    )
    eqs=[eq1,eq2,eq3]

    self.play(Write(eqs[0]))
    self.wait(0.5)
    for x in range(len(eqs)-1):
      self.play(TransformMatchingTex(eqs[x],eqs[x+1]))
      self.wait(0.5)
    self.play(FadeOut(eq3))
    self.wait(0.5)

    # Specialization
    eq4=MathTex(r'b-\text{proj}_{\text{col}(A)}b')
    eq5=MathTex(
      r'c_1\cdot ','(',r'b-\text{proj}_{\text{col}(A)}b',')',r'&=0\\',
      r'c_2\cdot ','(',r'b-\text{proj}_{\text{col}(A)}b',')',r'&=0\\',
      r'\vdots\\',
      r'c_n\cdot ','(',r'b-\text{proj}_{\text{col}(A)}b',')',r'&=0\\',
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
    eqs=[eq4,eq5,eq6,eq7]

    self.play(Write(eq4))
    self.wait(0.5)
    for x in range(len(eqs)-1):
      self.play(TransformMatchingTex(eqs[x],eqs[x+1]))
      self.wait(0.5)

class RightHandSideHelperScene(GridScene):
  def construct(self):
    # Draw column space of matrix A
    basis_vec=Vector([4,1])
    basis_vec_span=Line(
      start=-4*basis_vec.get_end(),
      end=4*basis_vec.get_end()
    )
    basis_span_label=MathTex(r'\text{col}(A)')
    basis_span_label.next_to(Dot([8,2,0]),DOWN)
    self.play(
      Create(basis_vec_span),
      FadeIn(basis_span_label)
    )
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

    # Draw b's projection onto column space of A
    proj_b_on_colA=self.projection(b,basis_vec)
    b_projection_helper=DashedLine(
      start=b.get_end(),
      end=proj_b_on_colA.get_end(),
      dash_length=0.2
    )
    proj_b_on_colA_label=MathTex(r'\text{proj}_{\text{col}(A)}b')
    proj_b_on_colA_label.next_to(b_projection_helper,DOWN*2)

    self.play(Create(b_projection_helper))
    self.wait(0.5)
    self.play(
      GrowArrow(proj_b_on_colA),
      FadeIn(proj_b_on_colA_label)
    )
    self.wait(0.5)

    # Draw component of b orthogonal to column space of A
    b_ort_comp=Vector(b.get_end()-proj_b_on_colA.get_end())
    b_ort_comp.shift(proj_b_on_colA.get_end())
    b_ort_comp_label=MathTex(r'b-\text{proj}_{\text{col}(A)}b')
    b_ort_comp_label.next_to(b_ort_comp,RIGHT)
    self.play(
      GrowArrow(b_ort_comp),
      FadeIn(b_ort_comp_label)
    )
    self.wait(0.5)

    # Draw right angle
    right_angle=RightAngle(b_ort_comp,basis_vec,length=0.4)
    self.play(FadeIn(right_angle))
    self.wait(0.5)
