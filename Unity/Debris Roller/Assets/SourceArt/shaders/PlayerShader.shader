// Upgrade NOTE: replaced '_Object2World' with 'unity_ObjectToWorld'
// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

Shader "Custom/PlayerShader" {
    Properties {
        _FresnelColor ("Fresnel Color", Color) = (1,1,1,1)
        _Opacity ("Opacity", Range(0, 5)) = 0.1773046
        _DiffuseColor ("Diffuse Color", Color) = (0.5,0.5,0.5,1)
        _Specularity ("Specularity", Range(0, 1)) = 0.6843017
        _Gloss ("Gloss", Range(0, 1)) = 0.1545734
    }
    SubShader {
        Tags {
            "IgnoreProjector"="True"
            "Queue"="Transparent"
            "RenderType"="Transparent"
        }
        LOD 200
        Pass {
            Name "FORWARD"
            Tags {
                "LightMode"="ForwardBase"
            }
            Blend One OneMinusSrcAlpha
            ZWrite Off
            
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #define UNITY_PASS_FORWARDBASE
            #include "UnityCG.cginc"
            #pragma multi_compile_fwdbase
            #pragma exclude_renderers gles3 metal d3d11_9x xbox360 xboxone ps3 ps4 psp2 
            #pragma target 3.0
            
            uniform float4 _LightColor0;
            uniform float4 _FresnelColor;
            uniform float _Opacity;
            uniform float4 _DiffuseColor;
            uniform half _Specularity;
            uniform half _Gloss;
            
            struct VertexInput {
                float4 vertex : POSITION;
                float3 normal : NORMAL;
            };
            
            struct VertexOutput {
                float4 pos : SV_POSITION;
                float4 posWorld : TEXCOORD0;
                float3 normalDir : TEXCOORD1;
            };
            
            VertexOutput vert (VertexInput v) {
                VertexOutput o = (VertexOutput)0;
                o.normalDir = UnityObjectToWorldNormal(v.normal);
                o.posWorld = mul(unity_ObjectToWorld, v.vertex);
                float3 lightColor = _LightColor0.rgb;
                o.pos = UnityObjectToClipPos(v.vertex);
                return o;
            }
            
            float4 frag(VertexOutput i) : COLOR {
                i.normalDir = normalize(i.normalDir);
				
				/////// Vectors:
                float3 viewDirection = normalize(_WorldSpaceCameraPos.xyz - i.posWorld.xyz);
                float3 normalDirection = i.normalDir;
                float3 lightDirection = normalize(_WorldSpaceLightPos0.xyz);
                float3 lightColor = _LightColor0.rgb;
                
                ////// Lighting:
                float attenuation = 1;
                float3 attenColor = attenuation * _LightColor0.xyz;
				
				///////// Gloss:
                float gloss = _Gloss;
                float specPow = exp2( gloss * 10.0+1.0);
				
				////// Specular:
                float NdotL = max(0, dot( normalDirection, lightDirection ));
                float3 specularColor = float3(_Specularity,_Specularity,_Specularity);
                float3 directSpecular = attenColor * pow(max(0,dot(reflect(-lightDirection, normalDirection),viewDirection)),specPow)*specularColor;
                float3 specular = directSpecular;
				
				/////// Diffuse:
                NdotL = max(0.0,dot( normalDirection, lightDirection ));
                float3 directDiffuse = max( 0.0, NdotL) * attenColor;
                float3 indirectDiffuse = UNITY_LIGHTMODEL_AMBIENT.rgb; // Ambient Light
                float3 diffuseColor = _DiffuseColor.rgb;
                float3 diffuse = (directDiffuse + indirectDiffuse) * diffuseColor;
				
				////// Emissive:
                float opacity = pow(1.0-max(0,dot(normalDirection, viewDirection)),_Opacity);
                float3 emissive = (_FresnelColor.rgb*opacity);
				
				/// Final Color:
                float3 finalColor = diffuse * opacity + specular + emissive;
                return fixed4(finalColor,opacity);
            }
            ENDCG
        }
    }
    FallBack "Diffuse"
}
