const formats={2:['getUint8',1],4:['getInt16',2],8:['getInt32',4],16:['getFloat32',4],64:['getFloat64',8],256:['getInt8',1],512:['getUint16',2],768:['getUint32',4]};
export function parseNifti(buffer){
 if(buffer.byteLength<352)throw Error('This file is too short to be a NIfTI volume.');
 const d=new DataView(buffer),le=d.getInt32(0,true)===348;
 if(d.getInt32(0,le)!==348)throw Error('Only NIfTI-1 single-file volumes are supported.');
 if(String.fromCharCode(...new Uint8Array(buffer,344,4))!=='n+1\0')throw Error('A single-file NIfTI-1 volume is required.');
 const dims=[1,2,3].map(i=>d.getInt16(40+i*2,le));
 if(d.getInt16(40,le)!==3||dims.some(n=>n<1||n>1024))throw Error('Use a 3D volume with dimensions up to 1024 voxels per axis.');
 const type=d.getInt16(70,le);if(!formats[type])throw Error('This NIfTI voxel datatype is not supported.');
 const [method,bytes]=formats[type],offset=d.getFloat32(108,le),count=dims.reduce((a,b)=>a*b);
 if(d.getInt16(72,le)!==bytes*8)throw Error('The voxel datatype and bit depth do not match.');
 if(!Number.isInteger(offset)||offset<352||offset+count*bytes>buffer.byteLength)throw Error('The volume is incomplete or has an invalid data offset.');
 const spacing=[1,2,3].map(i=>Math.abs(d.getFloat32(76+i*4,le)));
 if(spacing.some(v=>!Number.isFinite(v)||v<=0||v>100))throw Error('The volume has invalid voxel spacing.');
 let slope=d.getFloat32(112,le),inter=d.getFloat32(116,le);if(!slope){slope=1;inter=0;}
 if(!Number.isFinite(slope)||!Number.isFinite(inter))throw Error('Invalid intensity scaling.');
 const read=i=>d[method](offset+i*bytes,le)*slope+inter;
 let min=Infinity,max=-Infinity;for(let i=0;i<count;i+=Math.max(1,Math.floor(count/150000))){const v=read(i);if(Number.isFinite(v)){min=Math.min(min,v);max=Math.max(max,v);}}
 if(!Number.isFinite(min)||max<=min)throw Error('No usable intensity range was found in this volume.');
 return {dims,spacing,read,min,max,count};
}
export async function decodeFile(file){
 if(!/\.nii(\.gz)?$/i.test(file.name))throw Error('Choose a .nii or .nii.gz NIfTI-1 volume.');
 if(file.size>100*1024*1024)throw Error('Choose a file smaller than 100 MB.');
 let buffer=await file.arrayBuffer();
 if(/\.gz$/i.test(file.name)){
  if(typeof DecompressionStream==='undefined')throw Error('Your browser cannot decompress gzip. Use an uncompressed .nii file.');
  const reader=new Blob([buffer]).stream().pipeThrough(new DecompressionStream('gzip')).getReader();let size=0,chunks=[];
  try{while(true){const {done,value}=await reader.read();if(done)break;size+=value.length;if(size>200*1024*1024){await reader.cancel();throw Error('The uncompressed volume exceeds the 200 MB limit.');}chunks.push(value);}}catch(e){if(e.message.includes('200 MB'))throw e;throw Error('This gzip file is damaged or incomplete.');}
  buffer=await new Blob(chunks).arrayBuffer();
 }
 return parseNifti(buffer);
}
export function voxelPoints(scan,percent){
 const {dims,spacing,read,min,max,count}=scan,t=min+(max-min)*percent/100,step=Math.max(1,Math.ceil(Math.cbrt(count/130000))),points=[];
 const scale=4/Math.max(...dims.map((n,i)=>n*spacing[i]));
 for(let z=0;z<dims[2];z+=step)for(let y=0;y<dims[1];y+=step)for(let x=0;x<dims[0];x+=step){const v=read(x+dims[0]*(y+dims[1]*z));if(Number.isFinite(v)&&v>t)points.push((x-(dims[0]-1)/2)*spacing[0]*scale,(z-(dims[2]-1)/2)*spacing[2]*scale,-(y-(dims[1]-1)/2)*spacing[1]*scale);}
 return new Float32Array(points);
}
export function slicePixels(scan,axis,index,contrast=100){
 const {dims,spacing,read,min,max}=scan,axes=axis===2?[0,1]:axis===1?[0,2]:[1,2],width=dims[axes[0]],height=dims[axes[1]],data=new Uint8ClampedArray(width*height*4),range=(max-min)*contrast/100;
 for(let j=0;j<height;j++)for(let i=0;i<width;i++){const xyz=[0,0,0];xyz[axis]=index;xyz[axes[0]]=i;xyz[axes[1]]=height-1-j;const v=read(xyz[0]+dims[0]*(xyz[1]+dims[1]*xyz[2])),c=Number.isFinite(v)?Math.max(0,Math.min(255,(v-min)/range*255)):0,k=(i+j*width)*4;data[k]=data[k+1]=data[k+2]=c;data[k+3]=255;}
 return {width,height,data,ratio:width*spacing[axes[0]]/(height*spacing[axes[1]])};
}
