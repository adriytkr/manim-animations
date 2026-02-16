from manim import *

class GridScene(MovingCameraScene):
  def setup(self):
    self.grid=NumberPlane(
      x_range=[-14,14,1],
      y_range=[-14,14,1]
    )
    self.camera.frame.scale(1.3)
    self.add(self.grid)

class QuestionScene(Scene):
  def construct(self):
    self.wait(0.5)

    question=Paragraph(
      'How can we systematically construct an',
      'orthogonal basis from any given basis?',
      width=config.frame_width-1,
      t2c={
        'orthogonal basis':RED,
      },
      line_spacing=1,
      alignment='center'
    )

    self.play(Write(question))
    self.wait(0.5)

class HookScene(GridScene):
  def construct(self):
    self.wait(0.5)

    # First Basis Vector
    basis_v1=Vector([4,1])
    basis_v1_label=MathTex(r'v_1')
    basis_v1_label.next_to(basis_v1.get_end(),DOWN)

    # Second Basis Vector
    basis_v2=Vector([2,3])
    basis_v2_label=MathTex(r'v_2')
    basis_v2_label.next_to(basis_v2.get_end(),UP)

    # Draw Basis
    self.play(
      GrowArrow(basis_v1),
      GrowArrow(basis_v2),
      FadeIn(basis_v1_label,basis_v2_label)
    )
    self.wait(0.5)

    self.play(Blink(basis_v1,blinks=2,run_time=0.7))
    self.wait(0.5)

    self.play(Blink(basis_v2,blinks=2,run_time=0.7))
    self.wait(0.5)

    # Draw v1's span
    v=basis_v1.get_end()
    v1_span=Line(start=-4*v,end=4*v)
    v1_span.set_z_index(-1)
    self.play(Create(v1_span))
    self.wait(0.5)

    proj_v2_on_v1=Vector([40/17,10/17],color=RED)
    proj_v2_on_v1_raycast=DashedLine(
      start=basis_v2.get_end(),
      end=proj_v2_on_v1.get_end(),
      dash_length=0.21
    )
    proj_v2_on_v1_label=MathTex(r'\text{proj}_{\text{span}(v_1)}v_2',color=RED)
    proj_v2_on_v1_label.next_to(proj_v2_on_v1_raycast,DOWN*2)
    self.play(Create(proj_v2_on_v1_raycast))
    self.wait(0.5)
    self.play(
      GrowArrow(proj_v2_on_v1),
      FadeIn(proj_v2_on_v1_label)
    )
    self.wait(0.5)

    # Draw component of v2 orthogonal to v1's span
    v2_ort_comp=Vector([-6/17,41/17])
    v2_ort_comp.shift(proj_v2_on_v1.get_end())
    v2_ort_comp_label=MathTex(r'v_2-\text{proj}_{\text{span}(v_1)}v_2')
    v2_ort_comp_label.next_to((v2_ort_comp.get_start()+v2_ort_comp.get_end())/2,RIGHT)
    self.play(
      GrowArrow(v2_ort_comp),
      FadeIn(v2_ort_comp_label)
    )
    self.wait(0.5)

    # 'Clear' grid and move component of v2 orthogonal to v1's span to its own subspace
    self.play(
      FadeOut(
        v1_span,
        basis_v2,
        basis_v2_label,
        proj_v2_on_v1,
        proj_v2_on_v1_label,
        proj_v2_on_v1_raycast,
        v2_ort_comp_label,
      ),
    )
    tmp=v2_ort_comp.copy().shift(-proj_v2_on_v1.get_end())
    v2_ort_comp_label.next_to(
      (tmp.get_start()+tmp.get_end())/2,
      LEFT
    )
    self.play(
      v2_ort_comp.animate.shift(-proj_v2_on_v1.get_end()),
      FadeIn(v2_ort_comp_label)
    )
    self.wait(0.5)
    angle=RightAngle(
      basis_v1,
      v2_ort_comp,
      length=0.6,
      quadrant=(1,1),
      color=GREEN,
      fill_opacity=0,
    )
    self.play(FadeIn(angle))
    self.wait(0.5)

    # Orthonormal basis
    # basis_v1_normalized=Vector([4/np.sqrt(17),1/np.sqrt(17)])
    # v2_ort_normalized=Vector([-6/np.sqrt(1717),41/np.sqrt(1717)])
    # self.play(
    #   FadeOut(angle),
    #   Transform(basis_v1,basis_v1_normalized),
    #   Transform(v2_ort_comp,v2_ort_normalized),
    #   FadeOut(basis_v1_label,v2_ort_label)
    # )
    # basis_v1_normalized_label=MathTex(r'\frac{v_1}{\lVert v_1\rVert}')
    # v2_ort_normalized_label=MathTex(
    #   r'\frac{v_2-\text{proj}_{\text{span}(v_1)}v_2}'
    #   r'{\lVert v_2-\text{proj}_{\text{span}(v_1)}v_2\rVert}'
    # )

    # basis_v1_normalized_label.next_to((basis_v1_normalized.get_start()+basis_v1_normalized.get_end())/2,DOWN),
    # v2_ort_normalized_label.next_to(v2_ort_normalized.get_end(),LEFT)

    # self.play(FadeIn(basis_v1_normalized_label,v2_ort_normalized_label))
    # self.wait(0.5)

class TheoremScene(Scene):
  def construct(self):
    self.wait(0.5)

    # Theorem Introduction
    label1=MathTex(r'B=\{v_1,v_2,v_3,\dots,v_n\}')
    label1.to_edge(UP+LEFT*2)

    label2=MathTex(r'B^{\prime}=\{v_1^{\prime},v_2^{\prime},v_3^{\prime},\dots,v_n\}')
    label2.to_edge(UP+RIGHT*2)

    arrow=Arrow(
      start=label1.get_right(),
      end=label2.get_left(),
      buff=0.3
    )

    self.play(Write(label1))
    self.wait(0.5)
    self.play(GrowArrow(arrow))
    self.wait(0.5)
    self.play(Write(label2))
    self.wait(0.5)

    # Draw steps
    step1_text=MathTex(
      r'\text{Step 1: } v_1^{\prime}=v_1'
    )
    step2_text=MathTex(
      r'\text{Step 2: } v_2^{\prime}=v_2-\text{proj}_{\text{span}(v_1)}v_2'
    )
    step3_text=MathTex(
      r'\text{Step 3: } v_3^{\prime}=v_3-\text{proj}_{\text{span}(v_1,v_2)}v_3'
    )
    stepn_text=MathTex(
      r'\text{Step n: } v_n^{\prime}=v_n-\text{proj}_{\text{span}(v_1,v_2,\dots,v_{n-1})}v_n'
    )
    steps=[step1_text,step2_text,step3_text,stepn_text]
    etc=MathTex(r'\dots')

    g_steps=VGroup(step1_text,step2_text,step3_text,etc,stepn_text)
    g_steps.arrange(DOWN,aligned_edge=LEFT)
    g_steps.next_to(label1,DOWN,aligned_edge=LEFT)

    for step in steps[0:3]:
      self.play(Write(step))
      self.wait(0.5)

    self.play(Write(etc))
    self.wait(0.5)
    self.play(Write(steps[3]))
    self.wait(0.5)

class ProcessScene(Scene):
  def construct(self):
    self.wait(0.5)

    question=Paragraph(
      'Gram-Schmidt',
      'Process',
      font_size=64,
      line_spacing=1,
      alignment='center'
    )

    self.play(Write(question))
    self.wait(0.5)
